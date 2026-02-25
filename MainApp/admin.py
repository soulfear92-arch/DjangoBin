from django.contrib import admin
from .models import Comment, Snippet

# Register your models here.
#admin.site.register([Snippet, Comment])

@admin.register(Snippet)
class SnippetAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'lang', 'creation_date', 'is_public']
    list_filter = ['lang', 'creation_date']
    ordering = ['creation_date']
    search_fields = ['lang', 'code']


    
    
@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['text']
    search_fields = ['text']

    def has_image(self, obj):
        return '+' if obj.image else '-'
    has_image.short_description = 'Изображение'