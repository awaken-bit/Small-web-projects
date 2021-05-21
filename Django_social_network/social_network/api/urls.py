from django.contrib import admin
from django.urls import path
from . import views



urlpatterns = [
    path('posts/', views.LikeOrDizlikeView.as_view(), name='like_api'),
    path('comments/', views.CommentView.as_view(), name='comment_api'),
    path('dynamic_post_load/', views.DynamicPostLoad.as_view(), name='dynamic_post_load')
]