from django.shortcuts import render, redirect
from django.http import Http404
from django.utils import timezone
from .models import Snippet

def index_page(request):
    context = {'pagename': 'PythonBin'}
    return render(request, 'pages/index.html', context)

def add_snippet_page(request):
    if request.method == 'POST':
        snippet = Snippet(
            name=request.POST.get('name'),
            lang=request.POST.get('lang'),
            code=request.POST.get('code'),
            creation_date=timezone.now()
        )
        snippet.save()
        return redirect('mainapp:snippets_list')
    
    context = {'pagename': 'Добавление нового сниппета'}
    return render(request, 'pages/add_snippet.html', context)

def snippets_page(request):
    snippets = Snippet.objects.all()
    context = {
        'pagename': 'Просмотр сниппетов',
        'snippets': snippets
    }
    return render(request, 'pages/view_snippets.html', context)

def snippet_detail(request, snippet_id):
    try:
        snippet = Snippet.objects.get(id=snippet_id)
    except Snippet.DoesNotExist:
        raise Http404(f"Сниппет с номером {snippet_id} не найден")
    
    context = {
        'pagename': snippet.name,
        'snippet': snippet
    }
    return render(request, 'pages/snippet_detail.html', context)

def search_snippet(request):
    snippet_id = request.GET.get('snippet_id')
    
    if snippet_id and snippet_id.isdigit() and int(snippet_id) > 0:
        return redirect('mainapp:snippet_detail', snippet_id=int(snippet_id))
    return redirect('mainapp:index')