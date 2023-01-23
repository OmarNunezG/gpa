from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from core.models import Account


REGISTER_USER_URL = reverse("user:register")
CREATE_ACCOUNT_URL = reverse("account:create")


class AccountApiTests(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()

    def test_create_account_success(self):
        user_payload = {
            "first_name": "Test",
            "last_name": "Name",
            "username": "testuser",
            "email": "test@example.com",
            "password": "testP@ssword123",
        }
        res = self.client.post(REGISTER_USER_URL, user_payload)

        account_payload = {
            "username": "testuser",
            "current_balance": 2000,
        }

        res = self.client.post(CREATE_ACCOUNT_URL, account_payload)
        account = Account.objects.get(
            account_number=res.data["data"]["account_number"]
        )

        self.assertIn("account_number", res.data["data"])
        self.assertIn("current_balance", res.data["data"])
        self.assertIn("009150", res.data["data"]["account_number"])

        self.assertEqual(account.current_balance, 2000)
