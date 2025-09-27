from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.http import JsonResponse
from .models import Post, Comment
from .forms import CommentForm


def home(request):
    """Главная страница с последними опубликованными статьями"""
    posts = Post.objects.filter(is_published=True)[:5]
    return render(request, 'blog/home.html', {'posts': posts})


def post_list(request):
    """Список всех опубликованных статей"""
    posts = Post.objects.filter(is_published=True)
    return render(request, 'blog/post_list.html', {'posts': posts})


def post_detail(request, pk):
    """Детальная страница статьи с комментариями"""
    post = get_object_or_404(Post, pk=pk, is_published=True)
    comments = post.comments.all()
    
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            messages.success(request, 'Комментарий добавлен!')
            return redirect('post_detail', pk=post.pk)
    else:
        form = CommentForm()
    
    return render(request, 'blog/post_detail.html', {
        'post': post,
        'comments': comments,
        'form': form
    })


def register(request):
    """Регистрация нового пользователя"""
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, f'Добро пожаловать, {username}!')
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'blog/register.html', {'form': form})


@login_required
def my_posts(request):
    """Страница с постами текущего пользователя"""
    posts = Post.objects.filter(author=request.user)
    return render(request, 'blog/my_posts.html', {'posts': posts})


@login_required
def create_post(request):
    """Создание новой статьи"""
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        is_published = request.POST.get('is_published') == 'on'
        
        if title and content:
            post = Post.objects.create(
                title=title,
                content=content,
                author=request.user,
                is_published=is_published
            )
            messages.success(request, 'Статья создана!')
            return redirect('post_detail', pk=post.pk)
        else:
            messages.error(request, 'Заполните все обязательные поля!')
    
    return render(request, 'blog/create_post.html')


def api_posts(request):
    """API для получения списка статей (JSON)"""
    posts = Post.objects.filter(is_published=True)
    data = []
    for post in posts:
        data.append({
            'id': post.id,
            'title': post.title,
            'author': post.author.username,
            'created_at': post.created_at.isoformat(),
            'comment_count': post.comments.count()
        })
    return JsonResponse(data, safe=False)
