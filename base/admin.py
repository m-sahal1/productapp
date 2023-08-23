from django.contrib import admin
from .models import Category, Collection, Product, Variant, Image
# Register your models here.
admin.site.register(Category)
admin.site.register(Collection)
admin.site.register(Product)
admin.site.register(Variant)
admin.site.register(Image)