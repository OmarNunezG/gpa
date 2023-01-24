from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ["first_name", "last_name", "username", "password", "email"]
        extra_kwargs = {
            "password": {
                "write_only": True,
                "min_length": 8,  # Not working
            }
        }


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        serializer = UserSerializer(self.user, many=False)

        username = serializer.data.get("username")
        data["username"] = username

        return data
