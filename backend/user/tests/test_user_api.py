from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

REGISTER_USER_URL = reverse("user:register")
AUTH_URL = reverse("user:auth")


class UserApiTests(TestCase):
    def create_user(self, details):
        get_user_model().objects.create(
            first_name=details["first_name"],
            last_name=details["last_name"],
            username=details["username"],
            email=details["email"],
            password=details["password"],
        )

    def get_user(self, username):
        user = get_user_model().objects.get(username=username)
        return user

    def setUp(self) -> None:
        self.client = APIClient()

    def test_register_user_success(self):
        payload = {
            "first_name": "Test",
            "last_name": "Name",
            "username": "testusername",
            "email": "test@example.com",
            "password": "testP@ssword123",
        }

        res = self.client.post(REGISTER_USER_URL, payload)
        user = self.get_user(payload["username"])

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(res.data["status"], "success")
        self.assertNotIn("password", res.data["data"])
        self.assertTrue(
            user.check_password(payload["password"]),
        )

    def test_user_with_email_exists_error(self):
        payload = {
            "first_name": "Test",
            "last_name": "Name",
            "username": "testusername",
            "email": "test@example.com",
            "password": "testP@ssword123",
        }
        self.create_user(payload)
        res = self.client.post(REGISTER_USER_URL, payload)
        # user = self.get_user(payload["username"])

        self.assertEqual(res.status_code, status.HTTP_409_CONFLICT)
        # self.assertIsNone(user)

    def test_user_with_username_exists_error(self):
        payload = {
            "first_name": "Test",
            "last_name": "Name",
            "username": "testusername",
            "email": "test@example.com",
            "password": "testP@ssword123",
        }
        self.create_user(payload)
        res = self.client.post(REGISTER_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_409_CONFLICT)

    def test_generate_token_success(self):
        user_details = {
            "first_name": "Test",
            "last_name": "Name",
            "username": "testusername",
            "email": "test@example.com",
            "password": "testP@ssword123",
        }
        self.create_user(user_details)

        payload = {
            "username": user_details["username"],
            "password": user_details["password"],
        }
        res = self.client.post(AUTH_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data["status"], "success")
        self.assertIn("token", res.data["data"])

    def test_generate_token_bad_credentials(self):
        user_details = {
            "first_name": "Test",
            "last_name": "Name",
            "username": "testusername",
            "email": "test@example.com",
            "password": "goodpass",
        }
        self.create_user(user_details)

        payload = {
            "username": user_details["username"],
            "password": "badpass",
        }
        res = self.client.post(AUTH_URL, payload)

        self.assertNotIn("token", res.data["data"])
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_too_short_error(self):
        payload = {
            "first_name": "Test",
            "last_name": "Name",
            "username": "testusername",
            "email": "test@example.com",
            "password": "pw",
        }
        res = self.client.post(REGISTER_USER_URL, payload)

        user = self.get_user(username=payload["username"])
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertFalse(user)
