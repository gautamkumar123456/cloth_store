from django.dispatch import receiver
from django.db.models.signals import post_save, pre_save
from .models import *


@receiver(post_save, sender=CartItems)
def total_price(sender, **kwargs):
    cart_items = kwargs['instance']
    price_of_product = Products.objects.get(id=cart_items.products.id)
    cart_items.price = int(cart_items.quantity) * float(price_of_product.price)
    # cart = Cart.objects.get(id=cart_items.cart.id)
    # cart.total_price = cart_items.price
    # cart.save()
