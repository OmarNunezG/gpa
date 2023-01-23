from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from core.models import Account, Transaction
from account.serializers import AccountSerializer
from datetime import datetime

CREATE_ACCOUNT_URL = reverse("account:create")
TRANSFER_URL = reverse("transaction:transfer")


class AccountApiTests(TestCase):
    def create_user(self):
        user_info = {
            "first_name": "Test",
            "last_name": "Name",
            "username": "testuser",
            "email": "test@example.com",
            "password": "testP@ssword123",
        }

        user = get_user_model().objects.create(
            first_name=user_info["first_name"],
            last_name=user_info["last_name"],
            username=user_info["username"],
            email=user_info["email"],
            password=user_info["password"],
        )

        return user

    def create_admin_user(self):
        user_info = {
            "first_name": "Test",
            "last_name": "Name",
            "username": "testuser",
            "email": "test@example.com",
            "password": "testP@ssword123",
        }

        admin_user = get_user_model().objects.create(
            first_name=user_info["first_name"],
            last_name=user_info["last_name"],
            username=user_info["username"],
            email=user_info["email"],
            password=user_info["password"],
        )
        admin_user.is_staff = True
        admin_user.save()

    def setUp(self) -> None:
        self.client = APIClient()

    def test_create_account_success(self):
        self.create_admin_user()
        account_payload = {
            "username": "testuser",
            "current_balance": 2000,
        }

        # token =
        # self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token)
        res = self.client.post(CREATE_ACCOUNT_URL, account_payload)

        account = Account.objects.get(
            account_number=res.data["data"]["account_number"]
        )

        self.assertIn("account_number", res.data["data"])
        self.assertIn("current_balance", res.data["data"])
        self.assertIn("009150", res.data["data"]["account_number"])

        self.assertEqual(account.current_balance, 2000)

    def test_get_balance(self):
        self.create_user()
        account_payload = {
            "username": "testuser",
            "current_balance": 2000,
        }
        res = self.client.post(CREATE_ACCOUNT_URL, account_payload)
        account = res.data["data"]["account_number"]

        transaction_payload = {
            "transaction_type": "DEBIT",
            "note": "Store",
            "amount": 10,
            "account": account,
        }

        self.client.post(TRANSFER_URL, transaction_payload)

        GET_ACCOUNT_BALANCE_URL = reverse(
            "account:get_balance",
            kwargs={
                "account_number": account,
            },
        )

        res = self.client.get(f"{GET_ACCOUNT_BALANCE_URL}?date=23012023")

        self.assertEqual(
            1990,
            res.data["data"]["balance"],
        )
