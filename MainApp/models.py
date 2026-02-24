from django.db import models

class Snippet(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название")
    lang = models.CharField(max_length=30, default='python', verbose_name="Язык")
    code = models.TextField(max_length=5000, verbose_name="Код")
    creation_date = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    
    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['-creation_date']
        verbose_name = 'Сниппет'
        verbose_name_plural = 'Сниппеты'