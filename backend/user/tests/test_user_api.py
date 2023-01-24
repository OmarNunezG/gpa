from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

REGISTER_USER_URL = reverse("user:register")
AUTH_URL = reverse("user:token_obtain_pair")


class UserApiTests(APITestCase):
    def create_user(self, details, is_admin=False):
        user = get_user_model().objects.create(
            first_name=details["first_name"],
            last_name=details["last_name"],
            username=details["username"],
            email=details["email"],
            password=details["password"],
        )
        user.is_staff = is_admin
        user.is_superuser = is_admin
        user.save()
        return user

    def get_user(self, username):
        user = get_user_model().objects.get(username=username)
        return user

    def setUp(self) -> None:
        self.client = APIClient()

    def test_register_user_success(self):
        admin_payload = {
            "first_name": "Super",
            "last_name": "Name",
            "username": "superuser",
            "email": "super@example.com",
            "password": "testP@ssword123",
        }
        payload = {
            "first_name": "Test",
            "last_name": "Name",
            "username": "testusername",
            "email": "test@example.com",
            "password": "testP@ssword123",
        }

        admin = self.create_user(admin_payload, True)
        self.client.force_authenticate(admin)
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
        admin = self.create_user(payload, True)
        self.client.force_authenticate(admin)
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
        admin = self.create_user(payload, True)
        self.client.force_authenticate(admin)
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
        self.assertIn("refresh", res.data)
        self.assertIn("access", res.data)
