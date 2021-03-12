from django.urls import path
from . import views
urlpatterns = [
    path('', views.index, name='main'),
    path('new/<int:pk>', views.new_content, name='new')
]