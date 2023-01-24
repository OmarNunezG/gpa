from django.contrib.auth import get_user_model
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status
from account.serializers import AccountSerializer
from transaction.serializers import TransactionSerializer
from core.models import Account, Transaction
import random

# Create your views here.


@api_view(["POST"])
@permission_classes([IsAdminUser])
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
@permission_classes([IsAuthenticated])
def get_balance(request: Request, account_number):
    try:
        date = request.query_params.get("date")
        year, month, day = date[4:8], date[2:4], date[:2]

        user = request.user
        account = Account.objects.get(account_number=account_number)

        if account.user is not user:
            response = {
                "status": "fail",
                "data": {
                    "title": "Unauthorized",
                    "message": "",
                },
            }
            return Response(response, status=status.HTTP_401_UNAUTHORIZED)

        transaction = Transaction.objects.filter(
            account=account,
            date__year=year,
            date__month=month,
            date__day=day,
        ).latest("date")

        serializer = TransactionSerializer(transaction, many=False)

        response = {
            "status": "success",
            "data": {
                "balance": float(serializer.data["account_balance"]),
            },
        }

        return Response(response, status=status.HTTP_200_OK)
    except Exception as ex:
        print(ex)
        response = {
            "status": "error",
            "data": ex.args,
        }

        return Response(response, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def account_transactions(request: Request, account_number):
    try:
        user = request.user
        account = Account.objects.get(account_number=account_number)

        if account.user != user:
            response = {
                "status": "fail",
                "data": {
                    "title": "Invalid account",
                    "message": "This account does not exists.",
                },
            }
            return Response(response, status=status.HTTP_404_NOT_FOUND)

        transactions = Transaction.objects.filter(account=account)
        serializer = TransactionSerializer(transactions, many=True)

        response = {
            "status": "success",
            "data": {
                "transactions": serializer.data,
            },
        }
        return Response(response, status=status.HTTP_200_OK)
    except Exception as ex:
        response = {
            "status": "error",
            "data": {
                "message": f"Error, {ex}",
            },
        }
        return Response(response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
