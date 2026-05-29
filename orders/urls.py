from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views, api_views

app_name = 'orders'

router = DefaultRouter()
router.register(r'api/orders', api_views.OrderViewSet, basename='api_orders')

urlpatterns = [
    path('list/', views.order_list_view, name='order_list'),
    path('', include(router.urls)),
]