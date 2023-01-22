from rest_framework import serializers
from core.models import Transaction, TransactionType, Account
from account.serializers import AccountSerializer


class TransactionTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = TransactionType
        fields = ["transaction_type"]


class TransactionSerializer(serializers.ModelSerializer):
    transaction_type = serializers.SerializerMethodField(read_only=True)
    account = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Transaction
        fields = ["date", "transaction_type", "note", "amount", "account"]

    def get_transaction_type(self, obj):
        print(obj)
        transaction_type = obj.transaction_type
        serializer = TransactionTypeSerializer(transaction_type, many=False)
        return serializer.data

    def get_account(self, obj):
        print(obj)
        account = obj.account
        serializer = AccountSerializer(account, many=False)
        return serializer.data
