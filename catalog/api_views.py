from rest_framework import viewsets, permissions
from catalog.models import Category, Product
from drf_spectacular.utils import extend_schema, extend_schema_view
from .serializers import CatagorySerializer, ProductSerializer

@extend_schema_view(
    list=extend_schema(summary="Список категорий", tags=['Категории']),
    retrieve=extend_schema(summary="Детали категории", tags=['Категории']),
)
class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CatagorySerializer

@extend_schema_view(
    list=extend_schema(summary="Список товаров", tags=['Товары']),
    retrieve=extend_schema(summary="Детали товара", tags=['Товары']),
    create=extend_schema(summary="Создать товар", tags=['Товары']),
    update=extend_schema(summary="Обновить товар", tags=['Товары']),
    partial_update=extend_schema(summary="Частично обновить товар", tags=['Товары']),
    destroy=extend_schema(summary="Удалить товар", tags=['Товары']),
)
class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]