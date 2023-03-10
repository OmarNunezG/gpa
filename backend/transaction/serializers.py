from rest_framework import serializers
from core.models import Transaction
from account.serializers import AccountSerializer


class TransactionSerializer(serializers.ModelSerializer):
    account = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Transaction
        fields = [
            "ID",
            "date",
            "transaction_type",
            "note",
            "amount",
            "account_balance",
            "account",
        ]

    def get_account(self, obj: Transaction):
        account = obj.account
        serializer = AccountSerializer(account, many=False)
        return serializer.data["account_number"]
