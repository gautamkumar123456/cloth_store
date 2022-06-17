from django.urls import path
from .views import *

urlpatterns = [
    path('cart-view/', CartView.as_view({'get': 'list'}), name='cart'),
    path('cart-item-view/', CartItemView.as_view({'get': 'list'}), name='cart'),
    path('cart-item-delete/<int:pk>', CartItemsDeleteView.as_view({'post': 'destroy'}), name='delete-cart-items'),
    path('add-item/', CartItemsAddView.as_view({'post': 'create'}), name='cart-item'),
    path('cart-update/<int:pk>', CartItemsUpdateView.as_view({'put': 'partial_update'}), name='update-item')
]
