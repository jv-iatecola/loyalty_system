from django.db import models

class Accounts(models.Model):
    email = models.CharField(max_length=200, unique=True)
    password = models.CharField(max_length=200)
    username = models.CharField(max_length=200)
    id = models.CharField(max_length=200, primary_key=True)
    email_is_validated = models.BooleanField(False)
