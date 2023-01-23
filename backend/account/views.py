from django.contrib.auth import get_user_model
from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status
from account.serializers import AccountSerializer
from core.models import Account
from numpy import random, unique

# Create your views here.


@api_view(["POST"])
def create_account(request: Request):
    try:
        data = request.data

        account_number = f"009150{random.randint(1e9, 1e10)}"
        user = get_user_model().objects.get(username=data["username"])
        account = Account.objects.create(
            account_number=account_number,
            current_balance=data["current_balance"],
            user=user,
        )

        serializer = AccountSerializer(account, many=False)

        response = {
            "status": "success",
            "data": serializer.data,
        }

        return Response(response, status=status.HTTP_201_CREATED)
    except Exception as ex:
        response = {
            "status": "error",
            "data": ex.args,
        }

        return Response(response, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
def get_balance(self, date):
    pass
