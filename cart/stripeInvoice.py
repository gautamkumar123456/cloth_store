import stripe
from django.conf import settings

stripe.api_key = settings.STRIPE_SECRET_KEY


def invoice_sender(items, cart, user):
    pd = items
    product = stripe.Product.create(name=pd)
    price = stripe.Price.create(
        product=product.id,
        unit_amount=int(cart.total_price) * 100,
        currency="inr",
    )
    customer = stripe.Customer.create(
        name=user.first_name,
        email=user.email,
        description="My first customer",
    )

    stripe.InvoiceItem.create(
        customer=customer.id,
        price=price.id,
    )
    invoice = stripe.Invoice.create(
        customer=customer.id,
        collection_method="send_invoice",
        days_until_due=30,
    )
    stripe.Invoice.send_invoice(invoice.id)
    return
