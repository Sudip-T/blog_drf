from django.urls import reverse
from rest_framework import status
from blog_app.models import BlogPost
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token

User = get_user_model()

class BlogPostListCreateTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(email='test_user@example.com', password='testpassword')
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        self.url = reverse('post-list')

    def test_blog_post_list(self):
        BlogPost.objects.create(title='Post 1', author=self.user, content='test content 1')
        BlogPost.objects.create(title='Post 2', author=self.user, content='test content 2')
        response = self.client.get(self.url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_blog_post_create(self):
        data = {
            'title': 'Post 3',
            'content': 'test content 3',
            'is_active': True
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(BlogPost.objects.count(), 1)
        self.assertEqual(BlogPost.objects.get().title, 'Post 3')

    def test_unauthenticated_blog_post_create(self):
        self.client.logout()
        data = {
            'title': 'Post 4',
            'content': 'test content 4',
            'is_active': True
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_invalid_blog_post_data(self):
        data = {
            'title': '',
            'content': 'test content 4',
            'is_active': True
        }

        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('title', response.data)


class BlogPostDetailTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(email='user1@example.com', password='testpassword')
        self.user2 = User.objects.create_user(email='user2@example.com', password='otherpassword')
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        self.blog_post = BlogPost.objects.create(title='Test Post', author=self.user, content='Test content')
        self.url = reverse('post-detail', kwargs={'pk': self.blog_post.pk})  # Use the name you gave this URL in your urls.py

    def test_blog_post_retrieve(self):
        response = self.client.get(self.url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], self.blog_post.title)

    def test_blog_post_update(self):
        data = {
            'title': 'Updated Post',
            'content': 'Updated content',
            'is_active': True
        }
        response = self.client.put(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.blog_post.refresh_from_db()
        self.assertEqual(self.blog_post.title, 'Updated Post')
        self.assertEqual(self.blog_post.content, 'Updated content')

    def test_blog_post_update_unauthorized(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + Token.objects.create(user=self.user2).key)
        data = {
            'title': 'Unauthorized Update',
            'content': 'no update',
            'is_active': True
        }
        response = self.client.put(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_blog_post_delete(self):
        response = self.client.delete(self.url, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(BlogPost.objects.filter(pk=self.blog_post.pk).exists())

    def test_blog_post_delete_unauthorized(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + Token.objects.create(user=self.user2).key)
        response = self.client.delete(self.url, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertTrue(BlogPost.objects.filter(pk=self.blog_post.pk).exists())