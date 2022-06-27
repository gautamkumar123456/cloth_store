from accounts.models import User
from products.models import *
from django.core.validators import MinValueValidator, MaxValueValidator
from datetime import date


# Create your models here.
class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)
    total_price = models.FloatField(default=0)

    def __str__(self):
        return str(self.user)


class CartItems(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    products = models.ForeignKey(Products, on_delete=models.CASCADE)
    price = models.FloatField(default=0)
    quantity = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.user} {self.products}"


class AddressUser(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    area = models.CharField(max_length=50, null=False)
    landmark = models.CharField(max_length=50, null=False)
    city = models.CharField(max_length=50, null=False)
    pincode = models.IntegerField(validators=[MinValueValidator(6)])

    def __str__(self):
        return f"{str(self.user)} {self.area}"


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    address = models.ForeignKey(AddressUser, on_delete=models.PROTECT)
    items = models.TextField()
    ordered_on = models.DateField(auto_now=True, blank=True)

    def __str__(self):
        return f"{self.user}'s order"
