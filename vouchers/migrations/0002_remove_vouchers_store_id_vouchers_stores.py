# Generated by Django 5.0.3 on 2024-04-07 23:40

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stores', '0002_alter_stores_store_name'),
        ('vouchers', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='vouchers',
            name='store_id',
        ),
        migrations.AddField(
            model_name='vouchers',
            name='stores',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='stores.stores'),
        ),
    ]