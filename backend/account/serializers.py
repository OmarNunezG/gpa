from rest_framework import serializers
from core.models import Account


class AccountSerializer(serializers.ModelSerializer):
    current_balance = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Account
        fields = ["account_number", "current_balance"]

    def get_current_balance(self, obj: Account):
        current_balance = float(obj.current_balance)
        return current_balance
