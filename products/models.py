from django.db import models
from django.utils.text import slugify


# Create your models here.


class Category(models.Model):
    category_name = models.CharField(max_length=50)
    slug = models.SlugField(max_length=200, blank=True)
    """
    slug field is used to search in url. 
    """

    def save(self, *args, **kwargs):
        self.slug = slugify(self.category_name)
        super(Category, self).save(*args, **kwargs)

    def __str__(self):
        return self.category_name


class SubCategory(models.Model):
    season = models.CharField(max_length=10)

    def __str__(self):
        return self.season


class Brand(models.Model):
    brand = models.CharField(max_length=50)

    def __str__(self):
        return self.brand


class Size(models.Model):
    size = models.CharField(max_length=10)

    def __str__(self):
        return self.size


class Color(models.Model):
    color_name = models.CharField(max_length=20)

    def __str__(self):
        return self.color_name


class QualityType(models.Model):
    cloth_quality = models.CharField(max_length=20)

    def __str__(self):
        return self.cloth_quality


class Products(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE,null=False)
    season = models.ForeignKey(SubCategory, on_delete=models.CASCADE, null=False)
    product_name = models.CharField(max_length=100)
    product_img = models.ImageField(upload_to='product_img',null=False)
    price = models.IntegerField(null=False)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE,null=False)
    size = models.ForeignKey(Size, on_delete=models.CASCADE,null=False)
    color = models.ForeignKey(Color, on_delete=models.CASCADE,null=False)
    quality = models.ForeignKey(QualityType, on_delete=models.CASCADE, null=False)

    def __str__(self):
        return f"{self.product_name} {str(self.season)}"
