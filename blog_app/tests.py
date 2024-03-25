# blog/tests.py
from django.test import TestCase
from .models import Post
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token


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
