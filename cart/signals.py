from django.dispatch import receiver
from django.db.models.signals import post_save
from django.core.mail import EmailMessage
from cloth_store.settings import EMAIL_HOST_USER
from .models import *


@receiver(post_save, sender=Order)
def invoice_send(sender, instance, created, **kwargs):
    if created:
        subject = "Cloth_Store"
        body = f"Your order has been booked <br>" \
               f"Items are: {instance.items},<br>" \
               f"Total price:{instance.cart.total_price}<br>" \
               f"Thanks for booking"
        message = EmailMessage(
            subject,
            body,
            EMAIL_HOST_USER,
            [instance.user.email]
        )
        message.content_subtype = "html"
        message.send()
