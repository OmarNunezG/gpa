from rest_framework import serializers
from core.models import Transaction, TransactionType, Account
from account.serializers import AccountSerializer


class TransactionSerializer(serializers.ModelSerializer):
    account = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Transaction
        fields = ["date", "transaction_type", "note", "amount", "account"]

    def get_account(self, obj):
        print(obj)
        account = obj.account
        serializer = AccountSerializer(account, many=False)
        return serializer.data
