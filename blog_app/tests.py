# blog/tests.py
from django.test import TestCase
from .models import Post, Comment
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token

from .serializers import PostSerializer, CommentSerializer, UserSerializer


class PostModelTest(TestCase):
    class PostModelTest(TestCase):
        @classmethod
        def setUpTestData(cls):
            cls.post = Post.objects.create(title='Test Post', content='Test content')

        def test_post_content(self):
            self.assertEquals(self.post.title, 'Test Post')
            self.assertEquals(self.post.content, 'Test content')


class PostAPITests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='user', password='password')
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

    def test_create_post(self):
        url = reverse('post-list')
        data = {'title': 'New Post', 'content': 'Post content'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_list_posts(self):
        url = reverse('post-list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class UserRegistrationTest(APITestCase):
    def test_user_registration(self):
        url = reverse('register')
        data = {'username': 'newuser', 'password': 'newpassword', 'email': 'user@example.com'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue('token' in response.data)


class PostCreateTest(APITestCase):
    def test_create_post_unauthenticated(self):
        url = reverse('post-list')
        data = {'title': 'Title', 'content': 'Content'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class PostAccessTest(APITestCase):
    def test_unauthorized_access(self):
        response = self.client.get(reverse('post-list'))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class PostSerializerTest(TestCase):
    def setUp(self):
        self.post_attributes = {
            'title': 'Test Title',
            'content': 'Test Content',
        }
        self.post = Post.objects.create(**self.post_attributes)
        self.serializer = PostSerializer(instance=self.post)

    def test_contains_expected_fields(self):
        data = self.serializer.data
        self.assertEqual(set(data.keys()), set(['id', 'title', 'content', 'created_at', 'updated_at']))

    def test_title_field_content(self):
        data = self.serializer.data
        self.assertEqual(data['title'], self.post_attributes['title'])


class CommentSerializerTest(TestCase):
    def setUp(self):
        self.post = Post.objects.create(title='Test Post', content='Post Content')
        self.comment_attributes = {
            'post': self.post,
            'text': 'Main comment',
            'email': 'test@example.com',
        }
        self.comment = Comment.objects.create(**self.comment_attributes)
        self.reply = Comment.objects.create(**self.comment_attributes, parent=self.comment)
        self.serializer = CommentSerializer(instance=self.comment)

    def test_contains_expected_fields(self):
        data = self.serializer.data
        self.assertEqual(set(data.keys()), set(['id', 'post', 'parent', 'text', 'email', 'created_at']))


class UserSerializerTest(TestCase):
    def setUp(self):
        self.user_data = {
            'username': 'testuser',
            'password': 'testpassword123',
            'email': 'testuser@example.com',
        }
        self.serializer = UserSerializer(data=self.user_data)

    def test_serializer_valid(self):
        self.assertTrue(self.serializer.is_valid())

    def test_user_creation(self):
        self.serializer.is_valid()
        user = self.serializer.save()
        self.assertTrue(User.objects.filter(username='testuser').exists())
        self.assertTrue(user.check_password(self.user_data['password']))


from django.test import TestCase
from .tasks import add
from celery.result import EagerResult


class TestCeleryTask(TestCase):
    def test_add_task(self):
        task_result = add.apply(args=(10, 32))
        self.assertTrue(isinstance(task_result, EagerResult), "Task did not return an EagerResult")
        self.assertEqual(task_result.result, 42, "The add task did not return the correct sum")