from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from user.serializers import UserSerializer
from core.models import Account, Transaction
from account.serializers import AccountSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from user.serializers import CustomTokenObtainPairSerializer
from transaction.serializers import TransactionSerializer

# Create your views here.


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


@api_view(["POST"])
def register(request: Request):
    try:
        data = request.data
        user = get_user_model().objects.create(
            first_name=data["first_name"],
            last_name=data["last_name"],
            username=data["username"],
            email=data["email"],
            password=data["password"],
        )
        serializer = UserSerializer(user, many=False)

        response = {
            "status": "success",
            "data": serializer.data,
        }
        return Response(response, status=status.HTTP_201_CREATED)
    except Exception as ex:
        response = {
            "status": "error",
            "message": ex.args,
        }

        return Response(response, status=status.HTTP_409_CONFLICT)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def user_accounts(request: Request):
    try:
        user = request.user
        accounts = Account.objects.filter(user=user)
        account_serializer = AccountSerializer(accounts, many=True)
        user_serializer = UserSerializer(user, many=False)

        response = {
            "status": "success",
            "data": {
                "user": user_serializer.data["username"],
                "accounts": account_serializer.data,
            },
        }

        return Response(response, status=status.HTTP_200_OK)
    except Exception as ex:
        response = {
            "status": "error",
            "message": ex.args,
        }

        return Response(response, status=status.HTTP_409_CONFLICT)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def transactions(request: Request):
    try:
        user = request.user
        accounts = [account for account in Account.objects.filter(user=user)]

        transactions = Transaction.objects.filter(account=accounts)
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
