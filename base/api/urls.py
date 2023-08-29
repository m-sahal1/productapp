from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('products/', views.list_products, name='products'),
    path('variants/', views.list_variants, name='variants'),
    path('collections/', views.list_collections, name='collections'),
    path('collections/<str:pk>/products', views.list_collection_products, name='collection-of-products'),
    path('collections/<str:pk>/variations', views.list_collection_variations, name='collection-variations'),
    path('category/<str:pk>/variations', views.list_category_variations, name='category-variations'),
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
