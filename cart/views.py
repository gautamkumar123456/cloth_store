import datetime
from collections import Counter
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets, status
from rest_framework.response import Response
from .permissions import IsOwner
from .serializer import *

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
            product_item.total_price += quantity*cart_items.price
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
            Order_obj = Order.objects.create(user=user, cart=cart, address=address, items=items)
            cart.ordered = True
            cart.save()
            myData = OrderSerializer(Order_obj)
            return Response({'data': myData.data, 'msg': 'Order has been placed'})
        return Response({'msg': 'No cart is available'})


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
                    super(OrderCancel, self).destroy(request, *args, **kwargs)

                    cart.ordered = False
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
        return Response(
            {
                'products': trending_most
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
