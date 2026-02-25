from django.db import models
from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator
from django.core.exceptions import ValidationError

class Snippet(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название")
    lang = models.CharField(max_length=30, default='python', verbose_name="Язык")
    code = models.TextField(max_length=5000, verbose_name="Код")
    creation_date = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='snippets', null=True, blank=True)
    is_public = models.BooleanField(default=True, help_text="Если снято — сниппет виден только автору")
    
class Comment(models.Model):
    snippet = models.ForeignKey(
        'Snippet', 
        on_delete=models.CASCADE, 
        related_name='comments'
    )
    author = models.ForeignKey(
        User, 
        on_delete=models.CASCADE
    )
    text = models.TextField(max_length=500)
    image = models.ImageField(
        upload_to='comments/%Y/%m/%d/',
        blank=True,
        null=True,
        validators=[
            FileExtensionValidator(allowed_extensions=['png', 'jpg', 'jpeg', 'gif', 'webp']),
        ],
        help_text="Допустимые форматы: PNG, JPG, JPEG, GIF, WebP. Макс. размер: 2MB"
    )
    creation_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-creation_date']
        verbose_name = 'Сниппет'
        verbose_name_plural = 'Сниппеты'
    
    def __str__(self):
        return f'Комментарий {self.author.username} к сниппету #{self.snippet_id}'
    
    def clean(self):
        """Валидация размера файла на уровне модели"""
        if self.image and self.image.size > 2 * 1024 * 1024:
            from django.core.exceptions import ValidationError
            raise ValidationError({'image': 'Размер файла не должен превышать 2MB'})