from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from base.models import Category, Collection, Product, Variant
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework import status
from .serializers import ProductSerializer, VariantSerializer, CollectionSerializer, UserSerializer
from base.tasks import send_emails_everyone
from celery import Celery


class CustomAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        user_email = request.data["email"]
        user_password = request.data["password"]
        user= User.objects.get(email=user_email)
        user = authenticate(request, username=user.username, password =user_password)
        print(user)
        token, created = Token.objects.get_or_create(user=user)
        return Response({"token": token.key, "user_id": user.pk, "email": user.email})

@api_view(['POST'])
def register(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({'message':'user created'})
    return Response({'message':'user not created'})
    

@api_view(["GET"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def list_products(request):
    products = Product.objects.prefetch_related("variants", "variants__image").all()
    serializer = ProductSerializer(products, many=True)
    return Response(serializer.data)


@api_view(["GET"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def list_variants(request):
    variants = Variant.objects.select_related("image").all()
    serializer = VariantSerializer(variants, many=True)
    return Response(serializer.data)


@api_view(["GET"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def list_collections(request):
    collections = Collection.objects.all()
    serializer = CollectionSerializer(collections, many=True)
    return Response(serializer.data)


@api_view(["GET"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def list_collection_products(request, pk):
    collection = Collection.objects.prefetch_related(
        "products", "products__variants__image"
    ).get(id=pk)
    products = collection.products.all().values(
        "title", "description", "created_at", "updated_at", "variants__image__source"
    )
    return Response(products)


@api_view(["GET"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def list_collection_variations(request, pk):
    collection = Collection.objects.prefetch_related(
        "products__variants", "products__variants__image"
    ).get(id=pk)
    variants = Variant.objects.filter(product__in=collection.products.all()).values(
        "title",
        "created_at",
        "updated_at",
        "available_for_sale",
        "price",
        "image__source",
    )
    return Response(variants)


def get_category_ids(cat_id):
    cat_ids = []
    category = Category.objects.prefetch_related("category_set").get(id=cat_id)
    queue = [category]

    while queue:
        curr_cat = queue.pop(0)
        cat_ids.append(curr_cat.id)
        queue += [subcat for subcat in curr_cat.category_set.all()]

    return cat_ids


@api_view(["GET"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def list_category_variations(request, pk):
    category_ids = get_category_ids(pk)
    products = Product.objects.filter(category__in=category_ids).prefetch_related(
        "variants", "variants__image"
    )
    variants = Variant.objects.filter(product__in=products).values(
        "title",
        "created_at",
        "updated_at",
        "available_for_sale",
        "price",
        "image__source",
    )
    return Response(variants)

@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAdminUser])
def create_product(request):
    if request.method == 'POST':
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

@api_view(['PUT'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAdminUser])
def update_product(request, product_id):
    try:
        product = Product.objects.get(pk=product_id)
    except Product.DoesNotExist:
        return Response({'error': 'Product not found'}, status=404)
    
    if request.method == 'PUT':
        serializer = ProductSerializer(product, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAdminUser])
def create_variant(request, product_id):
    try:
        product = Product.objects.get(pk=product_id)
    except Product.DoesNotExist:
        return Response({'error': 'Product not found'}, status=404)
    
    if request.method == 'POST':
        variant_data = request.data
        variant_data['product'] = product.id
        serializer = VariantSerializer(data=variant_data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

@api_view(['PUT'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAdminUser])
def update_variant(request, variant_id):
    try:
        variant = Variant.objects.get(pk=variant_id)
    except Variant.DoesNotExist:
        return Response({'error': 'Variant not found'}, status=404)
    
    if request.method == 'PUT':
        serializer = VariantSerializer(variant, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)
    
@api_view(['POST'])
def send_mail_to_all(request):
    subject = request.data.get('subject')
    message = request.data.get('message')
    from_email = 'sahal9212500727@gmail.com'
    task_result = send_emails_everyone.delay(subject, message, from_email)
    
    return Response(
        {'message': 'Email sending task accepted', 'task_id': task_result.id},
        status=status.HTTP_202_ACCEPTED
    )
@api_view(['POST'])
def send_daily_email_updates_to_staff(request):
    prod_count= Product.objects.all().count()
    variant_count = Variant.objects.all().count()
    cust_count = User.objects.filter(is_staff = False).count()

    categories = Category.objects.all().prefetch_related('product_set')
    cat_wise_prod_count = "Category Name: \n"
    for cat in categories:
        cat_wise_prod_count += f"\t{cat.title}: {cat.product_set.all().count()}\n"
    subject = "Daily Updates"
    message = f'''
    Count of products: {prod_count}\n
    Count of variants: {variant_count}\n
    Count of products belonging to each category:\n{cat_wise_prod_count}\n
    Number of customers: {cust_count}\n
    '''
    recipient_emails = list(User.objects.filter(is_staff = True).values_list('email', flat = True))
    return send_emails_everyone.delay(subject, message, None, recipient_emails )
    