from django.db import models
from django.contrib.auth import get_user_model
import uuid


class Wallet(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    owner = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name="wallets", null=True, blank=True)
    available_funds = models.DecimalField(max_digits=14, decimal_places=2, default=0.00, null=True, blank=True)
    boxin_credits = models.DecimalField(max_digits=14, decimal_places=2, default=0.00, null=True, blank=True)
    escrow  = models.DecimalField(max_digits=14, decimal_places=2, blank=True, null=True)
    account_number = models.CharField(max_length=10, null=True, blank=True)
    bank = models.CharField(max_length=255, blank=True, null=True)
    bvn = models.CharField(max_length=11, blank=True, null=True)
    customer_code = models.CharField(max_length=255, blank=True, null=True)
    virtual_bank_account = models.CharField(max_length=10, blank=True, null=True)
    virtual_bank = models.CharField(max_length=225, blank=True, null=True)

    def __str__(self):
        return self.owner.firstname
