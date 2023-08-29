from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from base.models import Category, Collection, Product, Variant, Image
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import ProductSerializer, VariantSerializer, CollectionSerializer

@api_view(['GET'])
def list_products(request):
    products = Product.objects.prefetch_related('variants','variants__image').all()
    serializer = ProductSerializer(products, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def list_variants(request):
    variants= Variant.objects.select_related('image').all()
    serializer = VariantSerializer(variants, many= True)
    return Response(serializer.data)


@api_view(['GET'])
def list_collections(request):
    collections= Collection.objects.all()
    serializer = CollectionSerializer(collections, many = True)
    return Response(serializer.data)


@api_view(['GET'])
def list_collection_products(request, pk):
    collection= Collection.objects.prefetch_related('products','products__variants__image').get(id=pk)
    products= collection.products.all().values('title', 'description', 'created_at', 'updated_at', 'variants__image__source')
    return Response(products)


@api_view(['GET'])
def list_collection_variations(request, pk):
    collection= Collection.objects.prefetch_related('products__variants','products__variants__image').get(id=pk)
    variants = Variant.objects.filter(product__in=collection.products.all()).values(
        'title', 'created_at', 'updated_at', 'available_for_sale', 'price', 'image__source'
    )
    return Response(variants)


def get_category_ids(cat_id):
    cat_ids=[]
    category= Category.objects.prefetch_related('category_set').get(id=cat_id)
    queue=[category]

    while queue:
        curr_cat=queue.pop(0)
        cat_ids.append(curr_cat.id)
        queue+= [subcat for subcat in curr_cat.category_set.all()]

    return cat_ids
    
@api_view(['GET'])
def list_category_variations(request,pk):
    category_ids = get_category_ids(pk)
    products= Product.objects.filter(category__in = category_ids).prefetch_related('variants','variants__image')
    variants= Variant.objects.filter(product__in = products).values(
        'title', 'created_at', 'updated_at', 'available_for_sale', 'price', 'image__source'
        )
    return Response(variants)