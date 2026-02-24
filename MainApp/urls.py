from django.urls import path
from django.views.generic import RedirectView
from . import views

app_name = 'mainapp'

urlpatterns = [
    path('', views.index_page, name='index'),
     path('snippets/', RedirectView.as_view(
        pattern_name='mainapp:snippets_list',
        permanent=False
    )),
    path('snippets/add/', views.add_snippet_page, name='add_snippet'),
    path('snippets/list/', views.snippets_page, name='snippets_list'),
    path('snippets/<int:snippet_id>/', views.snippet_detail, name='snippet_detail'),
    path('snippets/search/', views.search_snippet, name='search_snippet'),
]