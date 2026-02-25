from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Snippet, Comment

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Пользователь с таким email уже существует")
        return email

LANGUAGE_CHOICES = [
    ('', 'Выберите язык...'),
    ('python', 'Python'),
    ('javascript', 'JavaScript'),
    ('java', 'Java'),
    ('cpp', 'C++'),
    ('c', 'C'),
    ('csharp', 'C#'),
    ('php', 'PHP'),
    ('ruby', 'Ruby'),
    ('go', 'Go'),
    ('rust', 'Rust'),
    ('swift', 'Swift'),
    ('kotlin', 'Kotlin'),
    ('typescript', 'TypeScript'),
    ('sql', 'SQL'),
    ('bash', 'Bash/Shell'),
    ('html', 'HTML'),
    ('css', 'CSS'),
    ('other', 'Другой'),
]

class SnippetForm(forms.ModelForm):
    class Meta:
        model = Snippet
        fields = ['name', 'lang', 'code', 'is_public']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Название сниппета'
            }),
            'lang': forms.Select(choices=LANGUAGE_CHOICES, attrs={
                'class': 'form-select'
            }),
            'code': forms.Textarea(attrs={
                'class': 'form-control font-monospace', 
                'rows': 15, 
                'placeholder': 'Ваш код...'
            }),
            'is_public': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
        }
        labels = {
            'is_public': 'Публичный сниппет (виден всем)',
        }
        help_texts = {
            'is_public': 'Если снять галочку — сниппет будет виден только вам',
        }

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text', 'image']
        widgets = {
            'text': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Ваш комментарий...',
                'maxlength': 500
            }),
            'image': forms.ClearableFileInput(attrs={
                'class': 'form-control',
                'accept': 'image/png,image/jpeg,image/gif,image/webp'
            }),
        }
        labels = {
            'image': '📎 Прикрепить изображение (опционально)',
        }
        help_texts = {
            'image': 'PNG, JPG, GIF, WebP. Макс. 2MB',
        }
    def clean_image(self):
        image = self.cleaned_data.get('image')
        
        if image:
            if image.size > 2 * 1024 * 1024:
                raise forms.ValidationError('Размер файла не должен превышать 2MB')
            allowed_mime_types = ['image/png', 'image/jpeg', 'image/gif', 'image/webp']
            if image.content_type not in allowed_mime_types:
                raise forms.ValidationError('Недопустимый формат изображения')
        return image