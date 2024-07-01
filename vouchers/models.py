from django.db import models
from accounts.models import Accounts
from stores.models import Stores


class Vouchers(models.Model):
    id = models.CharField(max_length=200, primary_key=True)
    # user_id = models.CharField(max_length=200)
    # store_id = models.CharField(max_length=200)
    created_at = models.CharField(max_length=200)
    accounts = models.ForeignKey(Accounts, on_delete=models.CASCADE, null=True)
    stores = models.ForeignKey(Stores, on_delete=models.CASCADE, null=True)
