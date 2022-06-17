from django_filters import rest_framework as filters
from .models import *


class ProductFilter(filters.FilterSet):
    min_price = filters.NumberFilter(field_name="price", lookup_expr='gte')
    max_price = filters.NumberFilter(field_name="price", lookup_expr='lte')
    category = filters.CharFilter(field_name='category__category_name', lookup_expr='iexact')
    brand = filters.CharFilter(field_name='brand__brand', lookup_expr='iexact')
    size = filters.CharFilter(field_name='size__size', lookup_expr='iexact')
    product_name = filters.CharFilter(field_name='product_name', lookup_expr='iexact')

    class Meta:
        model = Products
        exclude = ['product_img']
