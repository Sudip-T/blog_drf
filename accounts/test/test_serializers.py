from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model
from accounts.serializers import UserRegisterSerializer, UserLoginSerializer

User = get_user_model()


class UserRegisterSerializerTestCase(APITestCase):
    def test_valid_registration(self):
        data = {
            'email': 'blog_test@blog.com',
            'password': 'blog_test@!',
            'confirm_password': 'blog_test@!'
        }
        serializer = UserRegisterSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        user = serializer.save()
        self.assertEqual(user.email, data['email'])
        self.assertTrue(user.check_password(data['password']))
        self.assertEqual(serializer.errors, {})

    def test_existing_email(self):
        # Create a user with a specific email
        User.objects.create_user(email='blog_test@blog.com', password='blog_test@!')
        data = {
            'email': 'blog_test@blog.com',
            'password': 'blog_test@!',
            'confirm_password': 'blog_test@!'
        }
        serializer = UserRegisterSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('email', serializer.errors)

    def test_password_mismatch(self):
        data = {
            'email': 'blog_test@blog.com',
            'password': 'blog_test@!',
            'confirm_password': 'blog_test@!_2'
        }
        serializer = UserRegisterSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('password', serializer.errors)



class UserLoginSerializerTestCase(APITestCase):

    def setUp(self):
        # create user first
        self.user = User.objects.create_user(email='blog_test@blog.com', password='blog_test@!')

    def test_valid_login(self):
        data = {
            'email': 'blog_test@blog.com',
            'password': 'blog_test@!'
        }
        serializer = UserLoginSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        self.assertEqual(serializer.validated_data['user'], self.user)
        self.assertEqual(serializer.errors, {})

    def test_invalid_password(self):
        data = {
            'email': 'blog_test@blog.com',
            'password': 'dhsjddsdsd'
        }
        serializer = UserLoginSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('error', serializer.errors)
        self.assertEqual(serializer.errors['error'][0], 'Incorrect password.')

    def test_non_existent_user(self):
        data = {
            'email': 'hello@blog.com',
            'password': 'blog_test@!'
        }
        serializer = UserLoginSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('error', serializer.errors)
        self.assertEqual(serializer.errors['error'][0], 'user does not exist.')