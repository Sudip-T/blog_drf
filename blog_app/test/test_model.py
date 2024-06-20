import os
from time import sleep
from datetime import datetime
from django.test import TestCase
from django.conf import settings
from blog_app.models import BlogPost
from django.contrib.auth import get_user_model


User = get_user_model()

class BlogPostModelTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(email='testuser@example.com', password='password123')

    def test_blog_post_creation(self):
        blog_post = BlogPost.objects.create(
            title='Test Blog Post',
            author=self.user,
            content='This is a test blog post',
            is_active=True
        )

        self.assertEqual(blog_post.title, 'Test Blog Post')
        self.assertEqual(blog_post.author, self.user)
        self.assertEqual(blog_post.content, 'This is a test blog post')
        self.assertTrue(blog_post.is_active)
        self.assertIsNotNone(blog_post.created_on)

    def test_blog_post_str(self):
        blog_post = BlogPost.objects.create(
            title='Test Blog Post',
            author=self.user,
            content='This is a test blog post.'
        )
        self.assertEqual(str(blog_post), 'Test Blog Post')

    def test_blog_post_default_ordering(self):
        blog_post1 = BlogPost.objects.create(
            title='Post 1',
            author=self.user,
            content='This is an post 1',
            is_active=True,
            created_on=datetime.now()
        )
        sleep(1)
        blog_post2 = BlogPost.objects.create(
            title='Post 2',
            author=self.user,
            content='This is an post 2',
            is_active=True,
            created_on=datetime.now()
        )

        blog_posts = BlogPost.objects.all()
        self.assertEqual(blog_posts.first(), blog_post2)
        self.assertEqual(blog_posts.last(), blog_post1)

    def test_blog_post_image_field(self):
        image_path = os.path.join(settings.BASE_DIR, 'media/blogs/download.jpg')
        blog_post = BlogPost.objects.create(
            title='Blog Post test',
            author=self.user,
            content='This is a test blog post',
            image=image_path
        )
        self.assertEqual(blog_post.image, image_path)