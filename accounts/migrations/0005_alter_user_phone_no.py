# Generated by Django 3.2.13 on 2022-06-14 05:21

from django.db import migrations
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_alter_user_phone_no'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='phone_no',
            field=phonenumber_field.modelfields.PhoneNumberField(max_length=128, null=True, region=None),
        ),
    ]
