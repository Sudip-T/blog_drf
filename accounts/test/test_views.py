from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token

User = get_user_model()



class UserRegistrationViewTestCase(APITestCase):
    def setUp(self):
        self.url = reverse('register')

    def test_user_registration(self):
        data = {
            'email': 'blog_test@blog.com',
            'password': 'blog_test@!',
            'confirm_password': 'blog_test@!'
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('token', response.data)
        user = User.objects.get(email=data['email'])
        self.assertTrue(user.check_password(data['password']))

    def test_user_registration_existing_email(self):
        User.objects.create_user(email='blog_test@blog.com', password='blog_test@!')
        data = {
            'email': 'blog_test@blog.com',
            'password': 'blog_test@!',
            'confirm_password': 'blog_test@!'
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('email', response.data)

    def test_user_registration_password_mismatch(self):
        data = {
            'email': 'blog_test@blog.com',
            'password': 'blog_test@!',
            'confirm_password': 'blog_test@!000'
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('password', response.data)



class UserLoginViewTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(email='blog_test@blog.com', password='blog_test@')
        self.url = reverse('login_token')

    def test_user_login(self):
        data = {
            'email': 'blog_test@blog.com',
            'password': 'blog_test@'
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data)

    def test_user_login_invalid_password(self):
        data = {
            'email': 'blog_test@blog.com',
            'password': 'dshdhsdhsd'
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.data)

    def test_user_login_nonexistent_user(self):
        data = {
            'email': 'fjkjfkfjskf@example.com',
            'password': 'dsdjksdkjs'
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.data)



class LogoutViewTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(email='blog_test@blog.com', password='blog_test@')
        self.token = Token.objects.create(user=self.user)
        self.url = reverse('logout')

    def test_logout_success(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        response = self.client.post(self.url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(Token.objects.filter(user=self.user).exists())

    def test_logout_unauthenticated(self):
        self.client.logout()
        response = self.client.post(self.url, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)