from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APIClient, APITestCase
from rest_framework import status
from core.models import Account

AUTH_USER_URL = reverse("user:token_obtain_pair")
CREATE_ACCOUNT_URL = reverse("account:create")
REGISTER_USER_URL = reverse("user:register")
TRANSFER_URL = reverse("transaction:transfer")


class TransactionTests(APITestCase):
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

    def set_up_user(self):
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
            "username": "usertest",
            "current_balance": 2000,
        }

        user = self.create_user(register_user_payload, True)
        self.client.force_authenticate(user)
        self.client.post(AUTH_USER_URL, user_auth_payload)
        self.client.post(CREATE_ACCOUNT_URL, account_payload)
        self.user = self.get_user(register_user_payload["username"])

    def setUp(self) -> None:
        self.client = APIClient()
        self.set_up_user()

    def test_debit_transfer_success(self):
        account = Account.objects.get(user=self.user)
        transaction_payload = {
            "transaction_type": "DEBIT",
            "note": "Store",
            "amount": 10,
            "account": account.account_number,
        }

        res = self.client.post(TRANSFER_URL, transaction_payload)
        account = Account.objects.get(user=self.user)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual("success", res.data["status"])
        self.assertEqual(account.current_balance, 1990)

    def test_credit_transfer_success(self):
        account = Account.objects.get(user=self.user)
        transfer_payload = {
            "transaction_type": "CREDIT",
            "note": "Mom",
            "amount": 50,
            "account": account.account_number,
        }

        res = self.client.post(TRANSFER_URL, transfer_payload)
        account = Account.objects.get(user=self.user)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual("success", res.data["status"])
        self.assertEqual(account.current_balance, 2050)
