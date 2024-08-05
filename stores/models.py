from accounts.models import Accounts
from django.db import models

class Stores(models.Model):
    store_name = models.CharField(max_length=200, unique=True)
    id = models.CharField(max_length=200, primary_key=True)
    created_at = models.CharField(max_length=200)
    accounts = models.ForeignKey(Accounts, on_delete=models.CASCADE, null=True)
