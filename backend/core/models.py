from __future__ import annotations
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import (
    AbstractUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.db import models
from uuid import uuid4

# Create your models here.


class UserManager(BaseUserManager):
    def create(self, first_name, last_name, username, email, password) -> User:
        user = self.model(
            first_name=first_name,
            last_name=last_name,
            username=username,
            email=self.normalize_email(email),
        )
        user.set_password(password)
        user.save(using=self._db)

        return user

    def normalize_email(self, email: str):
        return email.lower()


class User(AbstractUser, PermissionsMixin):
    username_validator = UnicodeUsernameValidator()

    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    username = models.CharField(
        max_length=20,
        unique=True,
        validators=[username_validator],
    )
    email = models.EmailField(max_length=255, unique=True)

    objects = UserManager()

    REQUIRED_FIELDS = ["first_name", "last_name", "email"]

    def __str__(self) -> str:
        return self.username


class Account(models.Model):
    ID = models.AutoField(primary_key=True, unique=True, editable=False)
    account_number = models.CharField(
        max_length=16, unique=True, editable=False
    )
    current_balance = models.DecimalField(
        max_digits=100,
        decimal_places=4,
        default=0,
        validators=[MinValueValidator("0.01")],
    )
    user = models.ForeignKey(User, on_delete=models.PROTECT)

    def __str__(self) -> str:
        return self.account_number


class TransactionType(models.Model):
    ID = models.AutoField(primary_key=True, unique=True, editable=False)
    transaction_type = models.CharField(max_length=10)

    def __str__(self) -> str:
        return self.transaction_type


class Transaction(models.Model):
    ID = models.UUIDField(
        primary_key=True, default=uuid4, unique=True, editable=False
    )
    date = models.DateTimeField(auto_now_add=True)
    transaction_type = models.ForeignKey(
        TransactionType, on_delete=models.PROTECT
    )
    note = models.CharField(max_length=30)
    amout = models.DecimalField(
        max_digits=7,
        decimal_places=2,
        default=0,
        validators=[MinValueValidator("0.01"), MaxValueValidator("10000")],
    )
    account = models.ForeignKey(Account, on_delete=models.PROTECT)

    def __str__(self) -> str:
        return self.ID