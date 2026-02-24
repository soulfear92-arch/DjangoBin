from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Snippet

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
    ('', 'Выберите язык...'),  # Пустой вариант по умолчанию
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
            'is_public': '🌐 Публичный сниппет (виден всем)',
        }
        help_texts = {
            'is_public': 'Если снять галочку — сниппет будет виден только вам',
        }
