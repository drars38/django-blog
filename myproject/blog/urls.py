from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('posts/', views.post_list, name='post_list'),
    path('post/<int:pk>/', views.post_detail, name='post_detail'),
    path('register/', views.register, name='register'),
    path('my-posts/', views.my_posts, name='my_posts'),
    path('create-post/', views.create_post, name='create_post'),
    path('api/posts/', views.api_posts, name='api_posts'),
]

