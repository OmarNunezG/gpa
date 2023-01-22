from django.test import TestCase
from django.contrib.auth import get_user_model


class ModelsTests(TestCase):
    def test_create_user_success(self):
        first_name = "Test"
        last_name = "User"
        username = "testuser"
        email = "test@example.com"
        password = "testpass123"
        user = get_user_model().objects.create(
            first_name=first_name,
            last_name=last_name,
            username=username,
            email=email,
            password=password,
        )

        self.assertEqual(user.first_name, first_name)
        self.assertEqual(user.last_name, last_name)
        self.assertEqual(user.username, username)
        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))
