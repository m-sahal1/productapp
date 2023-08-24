from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from .models import Category, Collection, Product, Variant, Image


def list_products(request):
    products = Product.objects.prefetch_related('variants__image').all()
    # Shorten it with values method
    products_list = []
    for product in products:
        product_dict = {
            'title': product.title,
            'description': product.description,
            'created_at': product.created_at,
            'updated_at': product.updated_at,
            'images': [variant.image.source.url for variant in product.variants.all()]
        }
        products_list.append(product_dict)
    
    return JsonResponse(products_list, safe=False)


def list_variants(request):
    variants= Variant.objects.select_related('image').all()
    variants_dict_queryset=variants.values('title','created_at','updated_at', 'available_for_sale', 'price','image__source')
    variants_list=list(variants_dict_queryset)
    return JsonResponse(variants_list, safe=False)


def list_collections(request):
    collections= Collection.objects.all().values('title','published', 'updated_at')
    return JsonResponse(list(collections), safe=False)


def list_collection_products(request, pk):
    collection= Collection.objects.prefetch_related('products','products__variants__image').get(id=pk)
    products= collection.products.all().values('title', 'description', 'created_at', 'updated_at', 'variants__image__source')
    return JsonResponse(list(products), safe=False)


def list_collection_variations(request, pk):
    collection= Collection.objects.prefetch_related('products__variants','products__variants__image').get(id=pk)
    variants = Variant.objects.filter(product__in=collection.products.all()).values(
        'title', 'created_at', 'updated_at', 'available_for_sale', 'price', 'image__source'
    )
    return JsonResponse(list(variants), safe=False)




