from django.urls import path
from . import views



urlpatterns = [
    path('search_repositorys/', views.SearchRepositorys.as_view(), name='search_repositorys_api'),
]