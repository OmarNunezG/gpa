from django.contrib.auth import get_user_model, authenticate
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.request import Request
from rest_framework.response import Response
from user.serializers import UserSerializer

# Create your views here.


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
