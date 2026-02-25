from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import RegisterForm, SnippetForm, CommentForm
from django.utils import timezone
from .models import Snippet, Comment


def index_page(request):
    context = {'pagename': 'PythonBin'}
    return render(request, 'pages/index.html', context)

def snippets_page(request):
    lang_filter = request.GET.get('lang', '')
    sort_field = request.GET.get('sort', '-creation_date')
    allowed_sort_fields = ['id', 'name', 'lang', 'creation_date', '-id', '-name', '-lang', '-creation_date']
    if sort_field not in allowed_sort_fields:
        sort_field = '-creation_date'
    languages = Snippet.objects.values_list('lang', flat=True).distinct()
    if request.user.is_authenticated:
        snippets = Snippet.objects.filter(
            Q(is_public=True) | Q(author=request.user)
        ).select_related('author')
    else:
        snippets = Snippet.objects.filter(is_public=True).select_related('author')
    if lang_filter:
        snippets = snippets.filter(lang=lang_filter)
    snippets = snippets.order_by(sort_field).distinct()
    context = {
        'pagename': 'Просмотр сниппетов',
        'snippets': snippets,
        'is_my_snippets': False,
        'lang_filter': lang_filter,
        'languages': languages,
        'sort_field': sort_field,
    }
    return render(request, 'pages/view_snippets.html', context)


def snippet_detail(request, snippet_id):
    snippet = Snippet.objects.filter(id=snippet_id).first()
    if snippet is None:
        context = {
            'pagename': 'Сниппет не найден',
            'snippet_id': snippet_id,
        }
        return render(request, 'pages/snippet_not_found.html', context)
    context = {
        'pagename': snippet.name,
        'snippet': snippet,
    }
    return render(request, 'pages/snippet_detail.html', context)


def search_snippet(request):
    snippet_id = request.GET.get('snippet_id')
    
    if snippet_id and snippet_id.isdigit() and int(snippet_id) > 0:
        return redirect('mainapp:snippet_detail', snippet_id=int(snippet_id))
    return redirect('mainapp:index')


def register(request):
    if request.user.is_authenticated:
        return redirect('mainapp:index')
    
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f'🎉 Добро пожаловать, {user.username}!')
            return redirect('mainapp:index')
        else:
            messages.error(request, '❌ Исправьте ошибки в форме')
    else:
        form = RegisterForm()
    
    return render(request, 'pages/register.html', {'form': form, 'pagename': 'Регистрация'})

def my_snippets(request):
    lang_filter = request.GET.get('lang', '')
    sort_field = request.GET.get('sort', '-creation_date')
    allowed_sort_fields = ['id', 'name', 'lang', 'creation_date', '-id', '-name', '-lang', '-creation_date']
    if sort_field not in allowed_sort_fields:
        sort_field = '-creation_date'
    languages = Snippet.objects.values_list('lang', flat=True).distinct()
    snippets = Snippet.objects.filter(author=request.user).select_related('author')
    if lang_filter:
        snippets = snippets.filter(lang=lang_filter)
    snippets = snippets.order_by(sort_field).distinct()
    context = {
        'pagename': 'Мои сниппеты',
        'snippets': snippets,
        'is_my_snippets': True,
        'lang_filter': lang_filter,
        'languages': languages,
        'sort_field': sort_field,
    }
    return render(request, 'pages/view_snippets.html', context)


@login_required
def add_snippet_page(request):
    if request.method == 'POST':
        form = SnippetForm(request.POST)
        if form.is_valid():
            snippet = form.save(commit=False)
            snippet.author = request.user
            snippet.save()
            messages.success(request, 'Сниппет успешно создан!')
            return redirect('mainapp:my_snippets')
    else:
        form = SnippetForm()
    context = {'pagename': 'Добавление сниппета', 'form': form}
    return render(request, 'pages/add_snippet.html', context)

def snippet_edit(request, snippet_id):
    snippet = get_object_or_404(Snippet, id=snippet_id)
    if snippet.author != request.user:
        messages.error(request, 'Вы можете редактировать только свои сниппеты')
        return redirect('mainapp:snippet_detail', snippet_id=snippet_id)
    if request.method == 'POST':
        form = SnippetForm(request.POST, instance=snippet)
        if form.is_valid():
            form.save()
            messages.success(request, 'Сниппет обновлён!')
            return redirect('mainapp:snippet_detail', snippet_id=snippet.id)
        else:
            messages.error(request, 'Исправьте ошибки в форме')
    else:
        form = SnippetForm(instance=snippet)
    context = {
        'pagename': f'Редактирование: {snippet.name}',
        'form': form,
        'snippet': snippet,
        'is_editing': True,
    }
    return render(request, 'pages/add_snippet.html', context)

def snippet_delete(request, snippet_id):
    snippet = get_object_or_404(Snippet, id=snippet_id)
    if snippet.author != request.user:
        messages.error(request, '❌ Вы можете удалять только свои сниппеты')
        return redirect('mainapp:snippet_detail', snippet_id=snippet_id)
    if request.method == 'POST':
        snippet_name = snippet.name
        snippet.delete()
        messages.success(request, f'🗑️ Сниппет "{snippet_name}" удалён')
        return redirect('mainapp:my_snippets')
    context = {
        'pagename': 'Подтверждение удаления',
        'snippet': snippet,
    }
    return render(request, 'pages/snippet_confirm_delete.html', context)


def add_comment(request, snippet_id):
    snippet = get_object_or_404(Snippet, id=snippet_id)
    
    if request.method == 'POST':
        form = CommentForm(request.POST, request.FILES)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.snippet = snippet
            comment.author = request.user
            comment.save()
            messages.success(request, '✅ Комментарий добавлен!')
            return redirect('mainapp:snippet_detail', snippet_id=snippet_id)
        else:
            messages.error(request, '❌ Исправьте ошибки в форме')
    else:
        form = CommentForm()
    return redirect('mainapp:snippet_detail', snippet_id=snippet_id)