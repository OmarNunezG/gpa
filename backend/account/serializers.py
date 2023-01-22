from rest_framework import serializers
from core.models import Account


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ["account_number", "current_balance"]
