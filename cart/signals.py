from django.dispatch import receiver
from django.db.models.signals import post_save
from django.core.mail import EmailMessage
from cloth_store.settings import EMAIL_HOST_USER
from .models import *
import stripe
from django.conf import settings


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

#
# stripe.api_key = settings.STRIPE_SECRET_KEY
#
#
# @receiver(post_save, sender=Order)
# def invoice_sender(sender, instance, created, **kwargs):
#     print(created, kwargs)
#
#     if created:
#         print("hello")
#         pd = instance.items
#         product = stripe.Product.create(name=pd)
#         price = stripe.Price.create(
#             product=product.id,
#             unit_amount=int(instance.cart.total_price) * 100,
#             currency="inr",
#         )
#         customer = stripe.Customer.create(
#             name=instance.user.first_name,
#             email=instance.user.email,
#             description="My first customer",
#         )
#         print(customer.email)
#
#         stripe.InvoiceItem.create(
#             customer=customer.id,
#             price=price.id,
#         )
#         invoice = stripe.Invoice.create(
#             customer=customer.id,
#             collection_method="send_invoice",
#             days_until_due=30,
#         )
#         st = stripe.Invoice.send_invoice(invoice.id)
#         print(f"THE INVOICE DATA IS {st}")
