from django.contrib.auth import get_user_model, authenticate
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.request import Request
from rest_framework.response import Response
from user.serializers import UserSerializer
from rest_framework_simplejwt.tokens import RefreshToken

# Create your views here.


# @api_view(["POST"])
# def user_view(request: Request):
#     if request.method == "POST":
#         return register(request)


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


@api_view(["POST"])
def auth(request: Request):
    try:
        data = request.data
        user = authenticate(
            username=data["username"],
            password=data["password"],
        )

        if not user:
            response = {
                "status": "fail",
                "data": {
                    "title": "Authentication error",
                    "message": "Could not authenticate with provided credentials.",
                },
            }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)

        token = RefreshToken().for_user(user)

        response = {
            "status": "success",
            "data": {
                "token": {
                    "refresh": str(token),
                    "access": str(token.access_token),
                }
            },
        }
        return Response(response, status=status.HTTP_200_OK)
    except Exception as ex:
        response = {
            "status": "error",
            "message": ex.args,
        }
        return Response(response, status=status.HTTP_400_BAD_REQUEST)
