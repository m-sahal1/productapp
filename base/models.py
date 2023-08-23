# Django
# Design a Django Backend application that can store the following ecom related objects

# Product(title, description, created_at, updated_at)
# Variant(title, created_at, updated_at, available_for_sale, price)
# Image(source, alt_text, updated_at)
# Collection(title, published, updated_at)
# Categories/subcategories (title, created_at, updated_at)

# Conditions
# A product can have multiple variants but a variant can belong to only one product.
# A variant will always have an image associated with it
# Products can have zero or more images related to them which can be variant images
# A product can belong to multiple collections and a collection can contain multiple products.
# A product can belong to a category or subcategory.
# A Category can have n levels of subcategories.

from django.db import models

class Category(models.Model):
    title = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    parent = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.title

class Collection(models.Model):
    title = models.CharField(max_length=100)
    published = models.BooleanField(default=False)
    updated_at = models.DateTimeField(auto_now=True)
    products = models.ManyToManyField('Product', related_name='collections')

    def __str__(self):
        return self.title

class Product(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    category = models.ForeignKey('Category', on_delete=models.SET_NULL, null=True)
    def __str__(self):
        return self.title

class Variant(models.Model):
    title = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    available_for_sale = models.BooleanField(default=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='variants')
    image = models.OneToOneField('Image', on_delete=models.CASCADE)
    def __str__(self):
        return f"{self.title} Price:{self.price}"

class Image(models.Model):
    source = models.ImageField(upload_to='var_images/')
    alt_text = models.CharField(max_length=200)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.alt_text
