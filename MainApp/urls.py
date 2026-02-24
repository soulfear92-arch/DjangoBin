from django.urls import path
from django.views.generic import RedirectView
from django.contrib.auth import views as auth_views
from . import views

app_name = 'mainapp'

urlpatterns = [
    path('', views.index_page, name='index'),
     path('snippets/', RedirectView.as_view(
        pattern_name='mainapp:snippets_list',
        permanent=False
    )),
     path('login/', auth_views.LoginView.as_view(
        template_name='pages/login.html',
        redirect_authenticated_user=True
    ), name='login'),
    path('logout/', auth_views.LogoutView.as_view(
        next_page='mainapp:index'
    ), name='logout'),
    path('register/', views.register, name='register'),
    path('snippets/add/', views.add_snippet_page, name='add_snippet'),
    path('snippets/list/', views.snippets_page, name='snippets_list'),
    path('snippets/<int:snippet_id>/', views.snippet_detail, name='snippet_detail'),
    path('snippets/search/', views.search_snippet, name='search_snippet'),
    path('snippets/mine/', views.my_snippets, name='my_snippets'),
    path('snippets/<int:snippet_id>/edit/', views.snippet_edit, name='snippet_edit'),
    path('snippets/<int:snippet_id>/delete/', views.snippet_delete, name='snippet_delete'),
]