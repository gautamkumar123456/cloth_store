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
