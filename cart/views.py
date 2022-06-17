from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets, status
from rest_framework.response import Response
from .permissions import IsOwner
from .serializer import *


# Create your views here.

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


class CartItemView(viewsets.ModelViewSet):
    """
    This class is use for purpose of CartItem(Item of cart) View.
    """
    permission_classes = [IsOwner]
    serializer_class = CartItemsSerializer

    def list(self, request, *args, **kwargs):
        user = request.user
        cart = Cart.objects.filter(user=user, ordered=False).first()
        queryset = CartItems.objects.filter(cart=cart)
        serializer = CartItemsSerializer(queryset, many=True)
        return Response(serializer.data)


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
        price = product.price
        quantity = data.get('quantity')
        CartItems.objects.create(cart=cart, user=user, products=product, price=price, quantity=quantity)
        CartItems(price=price, products=product)
        CartItems.objects.filter(user=user, cart=cart.id)
        cart.total_price += float(price) * int(quantity)
        cart.save()
        return Response({'success': 'Items added to your cart'})


class CartItemsDeleteView(viewsets.ModelViewSet):
    """
    this class is used to delete cart items, but only by user whose cart item is available
    """
    permission_classes = (IsOwner,)
    serializer_class = CartItemsSerializer
    lookup_field = 'pk'

    def destroy(self, request, *args, **kwargs):
        data = kwargs['pk']  # here id of CartItems is storing
        cart_items = CartItems.objects.filter(id=data).first()
        if cart_items is not None:
            self.check_object_permissions(request, cart_items)
            """
            this is use for checking user is available for that given cartItem or No.
            """
            cart_items.delete()
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
        data = kwargs['pk']
        cart_items = CartItems.objects.filter(id=data).first()
        quantity = request.data.get('quantity')
        if cart_items is not None:
            self.check_object_permissions(request, cart_items)
            """
            this is use for checking user is available for that given cartItem or No.
            """
            cart_items.quantity += quantity
            cart_items.save()
            return Response({'message': 'Item updated successfully'}, status=status.HTTP_202_ACCEPTED)
        return Response({'message': 'No Item with given id'}, status=status.HTTP_404_NOT_FOUND)
