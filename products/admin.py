from django.contrib import admin
from .models import Products, Category, SubCategory, Color, Size, Brand, QualityType

# Register your models here.
admin.site.register(Products)
admin.site.register(Category)
admin.site.register(SubCategory)
admin.site.register(Color)
admin.site.register(Size)
admin.site.register(Brand)
admin.site.register(QualityType)
