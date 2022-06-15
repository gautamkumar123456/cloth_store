from rest_framework import serializers
from .models import *

"""
Serializer class for all views.
"""


class ProductSerializer(serializers.ModelSerializer):
    category = serializers.StringRelatedField()
    season = serializers.StringRelatedField()
    brand = serializers.StringRelatedField()
    size = serializers.StringRelatedField()
    color = serializers.StringRelatedField()
    quality = serializers.StringRelatedField()

    class Meta:
        model = Products
        fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class SizeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Size
        fields = '__all__'


class ColorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Color
        fields = '__all__'


class SeasonSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubCategory
        fields = '__all__'


class QualitySerializer(serializers.ModelSerializer):
    class Meta:
        model = QualityType
        fields = '__all__'


class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = '__all__'


class ProductSerializerView(serializers.ModelSerializer):
    """
    use of StringRelatedField() here to show their name. Without use of this these all fields present by its ID
    """
    category = CategorySerializer()
    season = SeasonSerializer()
    brand = BrandSerializer()
    size = SizeSerializer()
    color = ColorSerializer()
    quality = QualitySerializer()

    class Meta:
        model = Products
        fields = '__all__'
