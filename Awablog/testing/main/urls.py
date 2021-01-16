from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('blogs/',views.blogs_home, name='blogs_home'),
    path('blogs/<int:pk>/', views.blogsposts, name='blog_post'),
    path('post/<int:pk>/', views.BlogPost.as_view(), name='post_us'),
    path('post/<int:pk>/like', views.like, name='like'),
    path('post/<int:pk>/dizlike', views.dizlike, name='dizlike'),

    path('account/',views.dashboard,name='dashboard'),
    path('create/blog', views.create_blog, name='create_blog'),
    path('blogs/<int:pk>/create_post', views.create_post, name='create_post'),
    path('post/<int:pk>/delete_post', views.delete_post, name='delete_post'),
]
