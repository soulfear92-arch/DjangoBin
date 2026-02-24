from django.db import models
from django.contrib.auth.models import User

class Snippet(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название")
    lang = models.CharField(max_length=30, default='python', verbose_name="Язык")
    code = models.TextField(max_length=5000, verbose_name="Код")
    creation_date = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='snippets', null=True, blank=True)
    is_public = models.BooleanField(default=True, help_text="Если снято — сниппет виден только автору")
    
    class Meta:
        ordering = ['-creation_date']
        verbose_name = 'Сниппет'
        verbose_name_plural = 'Сниппеты'
    
    def __str__(self):
        return self.name