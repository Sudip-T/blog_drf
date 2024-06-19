from django.test import TestCase
from django.contrib.auth import get_user_model

User = get_user_model()


class UserModelTest(TestCase):
    def test_create_user(self):
        email = "test@tejjs0t.com"
        password = "testtest"

        user = User.objects.create_user(email=email, password=password)

        self.assertEqual(user.email, email)
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)
        self.assertTrue(user.check_password(password))

    def test_create_superuser(self):
        email = "admin@admin.com"
        password = "admin"

        superuser = User.objects.create_superuser(email=email, password=password)

        self.assertEqual(superuser.email, email)
        self.assertTrue(superuser.is_active)
        self.assertTrue(superuser.is_staff)
        self.assertTrue(superuser.is_superuser)
        self.assertTrue(superuser.check_password(password))