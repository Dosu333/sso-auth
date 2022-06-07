from attr import field
from rest_framework import serializers
from .models import *

class WalletSerializer(seriailizers.ModelSerializer):
    class Meta:
        model = Wallet
        fields = ('__all__')