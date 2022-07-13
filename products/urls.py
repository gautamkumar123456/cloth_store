from django.urls import path
from .views import *

urlpatterns = [
    path('product_views/', ProductViews.as_view({'get': 'list'}), name='products'),
    path('product_view_Id/', ProductViewId.as_view({'get': 'list', 'post': 'create'}), name='products'),
    path('product_view_Id/<int:pk>', ProductViewId.as_view({'put': 'partial_update', 'post': 'destroy'}),
         name='product'),
    path('category_view/', CategoryView.as_view({'get': 'list', 'post': 'create'}), name='category'),
    path('category_view/<int:pk>', CategoryView.as_view({'put': 'partial_update', 'post': 'destroy'}), name='category'),
    path('size_view/<int:pk>', SizeView.as_view({'put': 'partial_update', 'post': 'destroy'}), name='size'),
    path('size_view/', SizeView.as_view({'get': 'list', 'post': 'create'}), name='size'),
    path('color_view/<int:pk>', ColorView.as_view({'put': 'partial_update', 'post': 'destroy'}), name='color'),
    path('color_view/', ColorView.as_view({'get': 'list', 'post': 'create'}), name='color'),
    path('brand_view/<int:pk>', BrandView.as_view({'put': 'partial_update', 'post': 'destroy'}), name='brand'),
    path('brand_view/', BrandView.as_view({'get': 'list', 'post': 'create'}), name='brand'),
    path('season_view/<int:pk>', SeasonView.as_view({'put': 'partial_update', 'post': 'destroy'}), name='season'),
    path('season_view/', SeasonView.as_view({'get': 'list', 'post': 'create'}), name='season'),
    path('quality_view/<int:pk>', QualityView.as_view({'put': 'partial_update', 'post': 'destroy'}), name='quality'),
    path('quality_view/', QualityView.as_view({'get': 'list', 'post': 'create'}), name='quality')



]
