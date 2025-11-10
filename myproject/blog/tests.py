from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone
from .models import Post, Comment


class PostModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.post = Post.objects.create(
            title='Test Post',
            content='This is a test post content',
            author=self.user,
            is_published=True
        )

    def test_post_creation(self):
        """Тест создания поста"""
        self.assertEqual(self.post.title, 'Test Post')
        self.assertEqual(self.post.author, self.user)
        self.assertTrue(self.post.is_published)
        self.assertIsNotNone(self.post.created_at)

    def test_post_str_representation(self):
        """Тест строкового представления поста"""
        self.assertEqual(str(self.post), 'Test Post')

    def test_post_ordering(self):
        """Тест сортировки постов"""
        post2 = Post.objects.create(
            title='Test Post 2',
            content='Content 2',
            author=self.user,
            is_published=True
        )
        posts = Post.objects.all()
        self.assertEqual(posts[0], post2)  # Новый пост должен быть первым


class CommentModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.post = Post.objects.create(
            title='Test Post',
            content='This is a test post content',
            author=self.user,
            is_published=True
        )
        self.comment = Comment.objects.create(
            post=self.post,
            author=self.user,
            content='This is a test comment'
        )

    def test_comment_creation(self):
        """Тест создания комментария"""
        self.assertEqual(self.comment.post, self.post)
        self.assertEqual(self.comment.author, self.user)
        self.assertEqual(self.comment.content, 'This is a test comment')

    def test_comment_str_representation(self):
        """Тест строкового представления комментария"""
        expected = f"Комментарий от {self.user.username} к статье {self.post.title}"
        self.assertEqual(str(self.comment), expected)


class ViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.post = Post.objects.create(
            title='Test Post',
            content='This is a test post content',
            author=self.user,
            is_published=True
        )

    def test_home_view(self):
        """Тест главной страницы"""
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Добро пожаловать в мой блог!')
        self.assertContains(response, self.post.title)

    def test_post_list_view(self):
        """Тест страницы списка постов"""
        response = self.client.get(reverse('post_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Все статьи')
        self.assertContains(response, self.post.title)

    def test_post_detail_view(self):
        """Тест детальной страницы поста"""
        response = self.client.get(reverse('post_detail', args=[self.post.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.post.title)
        self.assertContains(response, self.post.content)

    def test_post_detail_view_404(self):
        """Тест 404 для несуществующего поста"""
        response = self.client.get(reverse('post_detail', args=[999]))
        self.assertEqual(response.status_code, 404)

    def test_register_view_get(self):
        """Тест GET запроса страницы регистрации"""
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Регистрация')

    def test_register_view_post(self):
        """Тест POST запроса регистрации"""
        data = {
            'username': 'newuser',
            'password1': 'newpass123',
            'password2': 'newpass123'
        }
        response = self.client.post(reverse('register'), data)
        self.assertEqual(response.status_code, 302)  # Редирект после успешной регистрации
        self.assertTrue(User.objects.filter(username='newuser').exists())

    def test_my_posts_view_requires_login(self):
        """Тест что страница моих постов требует авторизации"""
        response = self.client.get(reverse('my_posts'))
        self.assertEqual(response.status_code, 302)  # Редирект на страницу входа

    def test_my_posts_view_authenticated(self):
        """Тест страницы моих постов для авторизованного пользователя"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('my_posts'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Мои статьи')
        self.assertContains(response, self.post.title)

    def test_create_post_view_requires_login(self):
        """Тест что создание поста требует авторизации"""
        response = self.client.get(reverse('create_post'))
        self.assertEqual(response.status_code, 302)  # Редирект на страницу входа

    def test_create_post_view_authenticated(self):
        """Тест страницы создания поста для авторизованного пользователя"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('create_post'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Создать новую статью')

    def test_create_post_post_request(self):
        """Тест POST запроса создания поста"""
        self.client.login(username='testuser', password='testpass123')
        data = {
            'title': 'New Test Post',
            'content': 'This is new test content',
            'is_published': 'on'
        }
        response = self.client.post(reverse('create_post'), data)
        self.assertEqual(response.status_code, 302)  # Редирект после создания
        self.assertTrue(Post.objects.filter(title='New Test Post').exists())

    def test_api_posts_view(self):
        """Тест API для получения постов"""
        response = self.client.get(reverse('api_posts'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/json')
        data = response.json()
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]['title'], self.post.title)
        self.assertEqual(data[0]['author'], self.user.username)


class CommentTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.post = Post.objects.create(
            title='Test Post',
            content='This is a test post content',
            author=self.user,
            is_published=True
        )

    def test_add_comment_authenticated(self):
        """Тест добавления комментария авторизованным пользователем"""
        self.client.login(username='testuser', password='testpass123')
        data = {'content': 'Test comment'}
        response = self.client.post(reverse('post_detail', args=[self.post.pk]), data)
        self.assertEqual(response.status_code, 302)  # Редирект после добавления
        self.assertEqual(Comment.objects.count(), 1)
        comment = Comment.objects.first()
        self.assertEqual(comment.content, 'Test comment')
        self.assertEqual(comment.author, self.user)
        self.assertEqual(comment.post, self.post)


class IntegrationTests(TestCase):
    """Интеграционные тесты для проверки полного функционала"""
    
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )

    def test_full_blog_workflow(self):
        """Тест полного рабочего процесса блога"""
        # 1. Регистрация нового пользователя
        data = {
            'username': 'newuser',
            'password1': 'newpass123',
            'password2': 'newpass123'
        }
        response = self.client.post(reverse('register'), data)
        self.assertEqual(response.status_code, 302)
        
        # 2. Создание поста
        self.client.login(username='newuser', password='newpass123')
        post_data = {
            'title': 'Integration Test Post',
            'content': 'This is an integration test post',
            'is_published': 'on'
        }
        response = self.client.post(reverse('create_post'), post_data)
        self.assertEqual(response.status_code, 302)
        
        # 3. Проверка что пост появился в списке
        response = self.client.get(reverse('post_list'))
        self.assertContains(response, 'Integration Test Post')
        
        # 4. Добавление комментария
        post = Post.objects.get(title='Integration Test Post')
        comment_data = {'content': 'Great post!'}
        response = self.client.post(reverse('post_detail', args=[post.pk]), comment_data)
        self.assertEqual(response.status_code, 302)
        
        # 5. Проверка что комментарий добавился
        response = self.client.get(reverse('post_detail', args=[post.pk]))
        self.assertContains(response, 'Great post!')
        
        # 6. Проверка API
        response = self.client.get(reverse('api_posts'))
        data = response.json()
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]['comment_count'], 1)
