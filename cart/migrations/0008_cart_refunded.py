# Generated by Django 3.2.13 on 2022-07-11 10:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0007_order_payment_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='cart',
            name='refunded',
            field=models.BooleanField(default=False),
        ),
    ]