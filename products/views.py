from rest_framework.permissions import IsAdminUser
from rest_framework import viewsets
from .serializer import *
from .models import *
# Create your views here.


class ProductViewId(viewsets.ModelViewSet):
    permission_classes = [IsAdminUser]
    queryset = Products.objects.all()
    serializer_class = ProductSerializer


class ProductViews(viewsets.ModelViewSet):
    queryset = Products.objects.all()
    serializer_class = ProductSerializerView


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
