from django.contrib.auth import get_user_model
from rest_framework import serializers


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
