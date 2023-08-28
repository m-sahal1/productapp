from rest_framework import serializers
from base.models import Category, Collection, Product, Variant
class CategorySerializer(serializers.ModelSerializer):
    class META:
        model = Category
        fields = '__all__'