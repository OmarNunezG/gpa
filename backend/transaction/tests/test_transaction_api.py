from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from core.models import Account

AUTH_USER_URL = reverse("user:auth")
CREATE_ACCOUNT_URL = reverse("account:create")
REGISTER_USER_URL = reverse("user:register")
TRANSFER_URL = reverse("transaction:transfer")


class TransactionTests(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()

    def test_debit_transfer_success(self):
        register_user_payload = {
            "first_name": "user",
            "last_name": "Test",
            "username": "usertest",
            "email": "usertest@example.com",
            "password": "userpass",
        }

        user_auth_payload = {
            "username": "usertest",
            "password": "userpass",
        }

        account_payload = {
            "username": "testuser",
            "current_balance": 2000,
        }

        self.client.post(REGISTER_USER_URL, register_user_payload)
        self.client.post(AUTH_USER_URL, user_auth_payload)
        res = self.client.post(CREATE_ACCOUNT_URL, account_payload)

        user = get_user_model().objects.get(
            username=register_user_payload["username"]
        )
        for i in Account.objects.all():
            print(i)
        account = Account.objects.filter(user=user)

        transfer_payload = {
            "transaction_type": "DEBIT",
            "note": "Store",
            "amount": 10,
            "account": account.account_number,
        }

        res = self.client.post(TRANSFER_URL, transfer_payload)

        self.assertEqual(res.status_code, status=status.HTTP_200_OK)
        self.assertEqual("success", res.data["status"])
        self.assertEqual(account.current_balance, 1990)
