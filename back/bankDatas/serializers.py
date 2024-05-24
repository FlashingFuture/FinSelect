from rest_framework import serializers
from .models import FixedDeposit, SavingsAccount, Bank


class BankSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bank
        fields = '__all__'


class FixedDepositListSerializer(serializers.ModelSerializer):
    bank = BankSerializer(read_only=True)
    class Meta:
        model = FixedDeposit
        # fields = ('id')
        fields = '__all__'
  

class FixedDepositSerializer(serializers.ModelSerializer):
    bank = BankSerializer(read_only=True)
    class Meta:
        model = FixedDeposit
        fields = '__all__'


class SavingsAccountListSerializer(serializers.ModelSerializer):
    bank = BankSerializer(read_only=True)
    class Meta:
        model = SavingsAccount
        fields = '__all__'


class SavingsAccountSerializer(serializers.ModelSerializer):
    bank = BankSerializer(read_only=True)
    class Meta:
        model = SavingsAccount
        fields = '__all__'

