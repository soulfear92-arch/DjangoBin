from django.contrib import admin
from .models import Comment, Snippet

# Register your models here.
admin.site.register([Snippet, Comment])
