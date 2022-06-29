from .models import *
from products.serializer import *


class CartSerializer(serializers.ModelSerializer):
    user = serializers.CharField()

    class Meta:
        model = Cart
        # fields = '__all__'
        exclude = ['ordered']


class CartItemsSerializer(serializers.ModelSerializer):
    products = ProductSerializer()
    cart = CartSerializer()

    class Meta:
        model = CartItems
        fields = '__all__'


class AddressSerializer(serializers.ModelSerializer):

    class Meta:
        model = AddressUser
        fields = '__all__'


class OrderSerializer(serializers.ModelSerializer):
    user = serializers.CharField()
    address = serializers.CharField()
    cart = serializers.CharField()

    class Meta:
        model = Order
        fields = '__all__'


class FavouritesSerializer(serializers.ModelSerializer):
    products = serializers.CharField()

    class Meta:
        model = Favourites
        fields = '__all__'
