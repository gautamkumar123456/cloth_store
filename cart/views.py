import datetime
from collections import Counter
from django.views.decorators.csrf import csrf_exempt
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets, status
from rest_framework.response import Response
from django.http import JsonResponse, HttpResponse
from .permissions import IsOwner
from .serializer import *
from django.conf import settings
import stripe
from django.shortcuts import render
from .stripeutils import stripe_session_create
from .stripeInvoice import invoice_sender

"""
---------------------------------------------------CART--------------------------------------------------------
"""


class CartView(viewsets.ModelViewSet):
    """
    This class is use for purpose of Cart view.
    """
    permission_classes = [IsOwner]
    serializer_class = CartSerializer

    def list(self, request, *args, **kwargs):
        user = request.user
        queryset = Cart.objects.filter(user=user, ordered=False)
        serializer = CartSerializer(queryset, many=True)
        return Response(serializer.data)


"""
-------------------------------------------------------CART_ITEMS-----------------------------------------------
"""


class CartItemView(viewsets.ModelViewSet):
    """
    This class is use for purpose of CartItem(Item of cart) View.
    """
    permission_classes = [IsOwner]
    serializer_class = CartItemsSerializer

    def get_queryset(self):
        user = self.request.user
        cart = Cart.objects.filter(user=user, ordered=False).first()
        queryset = CartItems.objects.filter(cart=cart)
        return queryset


class CartItemsAddView(viewsets.ModelViewSet):
    """
    this class is used for adding items, after that each item is added to its own Cart.
    """
    permission_classes = [IsOwner]
    queryset = CartItems.objects.all()
    serializer_class = CartItemsSerializer
    lookup_field = 'pk'

    def create(self, request, *args, **kwargs):
        user = request.user
        data = request.data
        cart, _ = Cart.objects.get_or_create(user=user, ordered=False)
        product = Products.objects.get(id=data.get('product'))
        if product:
            price = product.price
            quantity = data.get('quantity')
            if quantity:
                CartItems.objects.create(cart=cart, user=user, products=product, price=price, quantity=quantity)
                CartItems(price=price, products=product)
                CartItems.objects.filter(user=user, cart=cart.id)
                cart.total_price += float(price) * int(quantity)
                cart.save()
                return Response({'success': 'Items added to your cart'})
            return Response({'msg': "Enter Quantity"})
        return Response({'msg': "Enter Product ID"})


class CartItemsDeleteView(viewsets.ModelViewSet):
    """
    this class is used to delete cart items, but only by user whose cart item is available
    """
    permission_classes = (IsOwner,)
    serializer_class = CartItemsSerializer
    lookup_field = 'pk'

    def destroy(self, request, *args, **kwargs):
        user = request.user
        data = kwargs['pk']  # here id of CartItems is storing
        cart_items = CartItems.objects.filter(id=data).first()
        if cart_items is not None:
            self.check_object_permissions(request, cart_items)
            """
            this is use for checking user is available for that given cartItem or No.
            """
            product_items = Cart.objects.filter(user=user, ordered=False).first()
            cart_items.delete()

            product_items.total_price -= cart_items.price * cart_items.quantity
            product_items.save()
            return Response({'message': 'Item deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
        return Response({'message': 'No Item with given id'}, status=status.HTTP_404_NOT_FOUND)


class CartItemsUpdateView(viewsets.ModelViewSet):
    """
    this class is used to update cart items, but only by user whose cart item is available
    """
    permission_classes = [IsAuthenticated, IsOwner]
    queryset = CartItems.objects.all()
    serializer_class = CartItemsSerializer
    lookup_field = 'pk'

    def partial_update(self, request, *args, **kwargs):
        user = request.user
        data = kwargs['pk']
        cart_items = CartItems.objects.filter(id=data).first()
        quantity = request.data.get('quantity')
        if cart_items is not None:
            self.check_object_permissions(request, cart_items)
            """
            this is use for checking user is available for that given cartItem or No.
            """
            product_item = Cart.objects.filter(user=user, ordered=False).first()
            cart_items.quantity += quantity
            cart_items.save()
            product_item.total_price += quantity * cart_items.price
            product_item.save()
            return Response({'message': 'Item updated successfully'}, status=status.HTTP_202_ACCEPTED)
        return Response({'message': 'No Item with given id'}, status=status.HTTP_404_NOT_FOUND)


"""
-------------------------------------------------ADDRESS-------------------------------------------------------
"""


class AddressCreate(viewsets.ModelViewSet):
    """
    This class is used for creating address.
    """
    permission_classes = [IsAuthenticated, IsOwner]
    queryset = AddressUser.objects.all()
    serializer_class = AddressSerializer
    lookup_field = 'pk'

    def create(self, request, *args, **kwargs):
        user = request.user
        data = request.data
        data['user'] = user.id
        serializer = self.serializer_class(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({'data': serializer.data, 'msg': 'Address has been created'})
        return Response({'data': serializer.errors, 'msg': 'Some error has occurred'})


class AddressView(viewsets.ModelViewSet):
    permission_classes = [IsOwner]
    queryset = AddressUser.objects.all()
    serializer_class = AddressSerializer
    lookup_field = 'pk'

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        super(AddressView, self).retrieve(request, *args, **kwargs)

        return Response(serializer.data)


class AddressUpdate(viewsets.ModelViewSet):
    """
    This class for updating address .
    """
    permission_classes = [IsOwner]
    queryset = AddressUser.objects.all()
    serializer_class = AddressSerializer
    lookup_field = 'pk'

    def partial_update(self, request, *args, **kwargs):
        super(AddressUpdate, self).partial_update(request, *args, **kwargs)
        return Response({'message': ' Address updated successfully'}, status=status.HTTP_202_ACCEPTED)


"""
-----------------------------------------------------ORDER---------------------------------------------------
"""


class OrderCreate(viewsets.ModelViewSet):
    """
    This class is for creating new order.
    """
    permission_classes = [IsOwner]
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    lookup_field = 'pk'

    def create(self, request, *args, **kwargs):
        user = request.user
        data = request.data
        address = AddressUser.objects.get(id=data.get('address'))
        cart = Cart.objects.filter(user=user, id=data.get('cart_id'), ordered=False).first()
        """
        Here Cart is filtered for checking that it is available or not.
        """
        if cart:
            items = cart.cartitems_set.values_list('products__product_name', flat=True)
            items = ",".join(items)
            order_obj = Order.objects.create(user=user, cart=cart, address=address, items=items)
            cart.ordered = True
            cart.save()
            myData = OrderSerializer(order_obj)
            stripe.api_key = settings.STRIPE_SECRET_KEY
            pay_data = {
                "price_data": {
                    "currency": "inr",
                    "unit_amount": int(cart.total_price) * 100,
                    "product_data": {
                        "name": cart,
                        "metadata": myData.data,
                    },
                },
                "quantity": 1
            }
            session = stripe_session_create(pay_data)
            customer = stripe.Customer.create(
                name=request.user.first_name,
                email=request.user.email,

            )
            stripe.PaymentIntent.create(
                customer=customer.id,
                receipt_email=request.user.email,
                payment_method_types=['card'],
                currency="inr",
                setup_future_usage='off_session',
                amount=int(cart.total_price * 100),

            )
            invoice_sender(items, cart, user)

            return JsonResponse({'id': session.url})
        return Response({'msg': 'No cart is available'})


@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None
    print("---------------------------------------------------------------")
    print("called")
    print("---------------------------------------------------------------")
    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
        )
    except ValueError:
        # Invalid payload
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError:
        # Invalid signature
        return HttpResponse(status=400)

    # Handle the checkout.session.completed event
    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        print(f"session payment :{session['payment_intent']}")
        payment_intent = stripe.checkout.Session.list(
            payment_intent=session["payment_intent"],
            expand=['data.line_items']
        )
        product_id = payment_intent['data'][0]['line_items']['data'][0]['price']['product']
        product = stripe.Product.retrieve(product_id)
        order_id = product['metadata']['id']
        order_obj = Order.objects.filter(id=order_id).first()
        if session.payment_status == "paid":
            order_obj.payment_id = session['payment_intent']
            order_obj.payed = True
            order_obj.save()

    elif event['type'] == 'checkout.session.async_payment_failed':
        session = event['data']['object']
        payment_intent = stripe.checkout.Session.list(
            payment_intent=session["payment_intent"],
            expand=['data.line_items']
        )
        product_id = payment_intent['data'][0]['line_items']['data'][0]['price']['product']
        product = stripe.Product.retrieve(product_id)
        order_id = product['metadata']['id']
        order_obj = Order.objects.filter(id=order_id).first()
        order_obj.payed = False
        order_obj.save()

    elif event["type"] == "charge.refunded":
        session = event['data']['object']
        order_obj = Order.objects.filter(payment_id=session['payment_intent']).first()
        order_obj.refund = True
        order_obj.payed = False
        order_obj.save()

    # TODO - send an email to the customer

    return HttpResponse(status=200)


def success_payment(request):
    return render(request, 'success.html')


def cancel_payment(request):
    return render(request, 'cancel.html')


class OrderView(viewsets.ModelViewSet):
    """
    This class is for specific order view by authorized user.
    """
    permission_classes = [IsAuthenticated, IsOwner]
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    lookup_field = 'pk'

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        super(OrderView, self).retrieve(request, *args, **kwargs)
        return Response(serializer.data)


class OrderCancel(viewsets.ModelViewSet):
    """
    This class is for purpose of cancel an order.
    """
    permission_classes = [IsOwner]
    serializer_class = OrderSerializer
    queryset = Order.objects.all()
    lookup_field = 'pk'

    def destroy(self, request, *args, **kwargs):
        user = request.user
        data = kwargs['pk']
        input_data = request.data
        cart_value = input_data['cart_id']
        if cart_value:
            order = Order.objects.filter(user=user, id=data).first()
            if order:
                self.check_object_permissions(request, order)
                cart = Cart.objects.filter(user=user, id=cart_value, ordered=True).first()
                if cart:
                    refund = stripe.Refund.create(payment_intent=order.payment_id)
                    if refund['status'] == "succeeded":
                        order.cancel = True
                        cart.ordered = False
                        order.save()
                        cart.save()
                        return Response({'message': ' Order has been cancelled successfully'},
                                        status=status.HTTP_202_ACCEPTED)
                return Response({'msg': 'No Cart is available'}, status=status.HTTP_404_NOT_FOUND)
            return Response({'msg': 'No Order is available'}, status=status.HTTP_404_NOT_FOUND)
        return Response({'msg': 'Please enter your cart ID'})


class TrendingProducts(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Order.objects.all()

    def list(self, request, *args, **kwargs):
        time_gap = datetime.date.today() - datetime.timedelta(days=7)
        orders = Order.objects.filter(ordered_on__gte=time_gap)
        dict_product = {}
        for order in orders:
            cart_items = CartItems.objects.filter(cart=order.cart)
            for cart_item in cart_items:
                if cart_item.products.id in dict_product:
                    dict_product[cart_item.products.id] += cart_item.quantity
                else:
                    dict_product[cart_item.products.id] = cart_item.quantity
        counting = Counter(dict_product)
        trending_most = counting.most_common(2)
        print(trending_most[0][0])
        return Response(
            {
                'products_id': trending_most[0][0], 'number_of_times_order': trending_most[0][1]
            }
        )


class FavouritesView(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, IsOwner]
    serializer_class = FavouritesSerializer
    lookup_field = 'pk'

    def create(self, request, *args, **kwargs):
        """
        This is used for creating favourites.
        """
        user = request.user
        data = request.data
        favourite_products = Products.objects.filter(id=data.get('fav_product')).first()
        if favourite_products:
            Fav_obj = Favourites.objects.create(user=user, products=favourite_products)
            myFav = FavouritesSerializer(Fav_obj)
            return Response({'Fav_products': myFav.data, 'msg': 'Product added to Favourites'})
        return Response({'msg': 'No Product is available for this ID'})

    def get_queryset(self):
        """
        This is used for getting list of all favourites.
        """
        user = self.request.user
        queryset = Favourites.objects.filter(user=user)
        return queryset
