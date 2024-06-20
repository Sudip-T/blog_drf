from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from blog_app.serializers import BlogPostSerializer
from blog_app.models import BlogPost

User = get_user_model()


class BlogPostSerializerTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(email='testuser@example.com', password='testpassword')
        self.valid_data = {
            'title': 'Test Blog Post',
            'author': self.user.id,
            'content': 'This is a test blog post content.',
            'is_active': True,
            'image': None
        }
        self.invalid_data = {
            'title': '',
            'author': self.user.id,
            'content': 'This is a test blog post content.',
            'is_active': True,
            'image': None
        }

    def test_valid_blog_post_creation(self):
        serializer = BlogPostSerializer(data=self.valid_data)
        self.assertTrue(serializer.is_valid())
        blog_post = serializer.save(author=self.user)  # Pass the user instance here
        self.assertEqual(blog_post.title, self.valid_data['title'])
        self.assertEqual(blog_post.author, self.user)
        self.assertEqual(blog_post.content, self.valid_data['content'])
        self.assertEqual(blog_post.is_active, self.valid_data['is_active'])
        self.assertEqual(serializer.errors, {})

    def test_invalid_blog_post_creation(self):
        serializer = BlogPostSerializer(data=self.invalid_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('title', serializer.errors)

    def test_read_only_fields(self):
        blog_post = BlogPost.objects.create(
            title='Test Blog Post',
            author=self.user,
            content='This is a test blog post content.',
            is_active=True
        )
        serializer = BlogPostSerializer(blog_post, data={'id': 999, 'author': 999}, partial=True)
        self.assertTrue(serializer.is_valid())
        updated_blog_post = serializer.save()
        self.assertNotEqual(updated_blog_post.id, 999)
        self.assertNotEqual(updated_blog_post.author.id, 999)

    def test_partial_update(self):
        blog_post = BlogPost.objects.create(
            title='Test Blog Post',
            author=self.user,
            content='This is a test blog post content.',
            is_active=True
        )
        updated_data = {'title': 'Updated Title'}
        serializer = BlogPostSerializer(blog_post, data=updated_data, partial=True)
        self.assertTrue(serializer.is_valid())
        updated_blog_post = serializer.save()
        self.assertEqual(updated_blog_post.title, updated_data['title'])
        self.assertEqual(updated_blog_post.content, 'This is a test blog post content.')  # unchanged fields
        self.assertEqual(updated_blog_post.is_active, True)

    def test_complete_update(self):
        blog_post = BlogPost.objects.create(
            title='Test Blog Post',
            author=self.user,
            content='This is a test blog post content.',
            is_active=True
        )
        updated_data = {
            'title': 'Updated Title',
            'content': 'Updated content.',
            'is_active': False,
        }
        serializer = BlogPostSerializer(blog_post, data=updated_data)
        self.assertTrue(serializer.is_valid())
        updated_blog_post = serializer.save()
        self.assertEqual(updated_blog_post.title, updated_data['title'])
        self.assertEqual(updated_blog_post.content, updated_data['content'])
        self.assertEqual(updated_blog_post.is_active, updated_data['is_active'])

