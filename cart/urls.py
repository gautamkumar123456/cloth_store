from django.urls import path
from .views import CartView,CartItemView,CartItemsUpdateView,CartItemsDeleteView,CartItemsAddView,AddressView,\
    AddressUpdate,AddressCreate,OrderCreate,OrderView,OrderCancel,TrendingProducts,FavouritesView,success_payment,\
    cancel_payment,stripe_webhook

urlpatterns = [
    path('cart-view/', CartView.as_view({'get': 'list'}), name='cart'),
    path('cart-item-view/', CartItemView.as_view({'get': 'list'}), name='cart'),
    path('cart-item-delete/<int:pk>', CartItemsDeleteView.as_view({'post': 'destroy'}), name='delete-cart-items'),
    path('add-item/', CartItemsAddView.as_view({'post': 'create'}), name='cart-item'),
    path('cart-update/<int:pk>', CartItemsUpdateView.as_view({'put': 'partial_update'}), name='update-item'),
    path('address-view/', AddressView.as_view({'get': 'retrieve'}), name='address-view'),
    path('address-create/', AddressCreate.as_view({'post': 'create'}), name='address-create'),
    path('address-view/<int:pk>', AddressView.as_view({'get': 'retrieve'}), name='address-view'),
    path('address-views/', AddressView.as_view({'get': 'list'}), name='address-views'),
    path('address-update/<int:pk>', AddressUpdate.as_view({'put': 'partial_update'}), name='address-update'),
    path('order-create/', OrderCreate.as_view({'post': 'create'}), name='order-create'),
    path('order-views/', OrderView.as_view({'get': 'list'}), name='order-views'),
    path('order-cancel/<int:pk>', OrderCancel.as_view({'post': 'destroy'}), name='order-cancel'),
    path('trending/', TrendingProducts.as_view({'get': 'list'}), name='trending-product'),
    path('favourites/', FavouritesView.as_view({'post': 'create', 'get': 'list'})),
    path('favourites_del/<int:pk>', FavouritesView.as_view({'post': 'destroy'})),
    # path('checkout/', create_checkout_session, name='checkout'),
    path('success/', success_payment),
    path('cancel/', cancel_payment),
    path('webhook/', stripe_webhook),

]
