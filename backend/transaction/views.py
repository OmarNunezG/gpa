from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.request import Request
from rest_framework.response import Response
from transaction.serializers import TransactionSerializer
from core.models import Transaction, Account
from decimal import Decimal

# Create your views here.


@api_view(["POST"])
def transfer(request: Request):
    try:
        data = request.data
        account = Account.objects.get(
            account_number=data["account"],
        )

        if not account:
            response = {
                "status": "fail",
                "data": {
                    "title": "Account not found",
                    "message": "Account was not found. Please, check account number was correct.",
                },
            }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)

        amount = Decimal(data["amount"])

        if data["transaction_type"] == "CREDIT":
            account.current_balance += amount

        if data["transaction_type"] == "DEBIT":
            if account.current_balance < amount:
                response = {
                    "status": "fail",
                    "data": {
                        "title": "Insuficient founds",
                        "message": "Account does not have suficient founds to finish the transaction.",
                    },
                }
                return Response(
                    response, status=status.HTTP_402_PAYMENT_REQUIRED
                )
            account.current_balance -= amount
        account.save()

        transaction = Transaction.objects.create(
            transaction_type=data["transaction_type"],
            note=data["note"],
            amount=amount,
            account=account,
        )

        serializer = TransactionSerializer(transaction, many=False)

        response = {
            "status": "success",
            "data": serializer.data,
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
