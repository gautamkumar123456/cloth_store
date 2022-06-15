from rest_framework.permissions import IsAdminUser
from rest_framework import viewsets
from rest_framework.response import Response

from .serializer import *
from .models import *


# Create your views here.


class ProductViewId(viewsets.ModelViewSet):
    permission_classes = [IsAdminUser]
    queryset = Products.objects.all()
    serializer_class = ProductSerializerView


class ProductViews(viewsets.ModelViewSet):
    serializer_class = ProductSerializer

    def list(self, request, *args, **kwargs):
        category = self.request.query_params.get('category')
        if category:
            """
            Filter method is used to search products category wise.
            """
            queryset = Products.objects.filter(category__category_name__iexact=category)
        else:
            queryset = Products.objects.all()
        serializer = ProductSerializer(queryset, many=True)
        return Response({'data': serializer.data, 'count': len(serializer.data)})


class CategoryView(viewsets.ModelViewSet):
    permission_classes = [IsAdminUser]
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class SizeView(viewsets.ModelViewSet):
    permission_classes = [IsAdminUser]
    queryset = Size.objects.all()
    serializer_class = SizeSerializer


class ColorView(viewsets.ModelViewSet):
    permission_classes = [IsAdminUser]
    queryset = Color.objects.all()
    serializer_class = ColorSerializer


class BrandView(viewsets.ModelViewSet):
    permission_classes = [IsAdminUser]
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer


class SeasonView(viewsets.ModelViewSet):
    permission_classes = [IsAdminUser]
    queryset = SubCategory.objects.all()
    serializer_class = SeasonSerializer


class QualityView(viewsets.ModelViewSet):
    permission_classes = [IsAdminUser]
    queryset = QualityType.objects.all()
    serializer_class = QualitySerializer

