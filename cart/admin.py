from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Cart)
admin.site.register(CartItems)
admin.site.register(Order)
admin.site.register(AddressUser)
admin.site.register(Favourites)
