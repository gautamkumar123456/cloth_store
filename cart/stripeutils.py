import stripe
from django.conf import settings


def stripe_session_create(data):
    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[data],
        mode='payment',
        success_url=f"{settings.DOMAIN}api/cart/success",
        cancel_url=f"{settings.DOMAIN}api/cart/cancel",
    )
    return session
