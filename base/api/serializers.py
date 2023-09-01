from rest_framework import serializers
from base.models import Category, Collection, Product, Variant, Image
from django.contrib.auth.models import User
from rest_framework.validators import UniqueValidator

class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ["source", "alt_text"]


class VariantSerializer(serializers.ModelSerializer):
    image = ImageSerializer()

    class Meta:
        model = Variant
        fields = [
            "title",
            "created_at",
            "updated_at",
            "available_for_sale",
            "price",
            "image",
        ]


class ProductSerializer(serializers.ModelSerializer):
    variants = VariantSerializer(many=True, required=False)

    class Meta:
        model = Product
        fields = ["title", "description", "created_at", "updated_at", "variants"]


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"


class CollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Collection
        fields = ["title", "published", "updated_at"]

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields= ['username', 'email', 'password']
        extra_kwargs = {
            'email': {
                'validators': [UniqueValidator( queryset= User.objects.all())]
            }
        }