from rest_framework import viewsets, permissions
from orders.models import Order
from .serializers import OrderSerializer
from drf_spectacular.utils import extend_schema, extend_schema_view

@extend_schema_view(
    list=extend_schema(summary="Список заказов", tags=['Заказы']),
    retrieve=extend_schema(summary="Детали заказа", tags=['Заказы']),
    create=extend_schema(summary="Создать заказ", tags=['Заказы']),
    update=extend_schema(summary="Обновить заказ", tags=['Заказы']),
    partial_update=extend_schema(summary="Частично обновить заказ", tags=['Заказы']),
    destroy=extend_schema(summary="Удалить заказ", tags=['Заказы']),
)
class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]