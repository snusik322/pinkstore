from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views, api_views

app_name = 'catalog'

router = DefaultRouter()
router.register(r'api/categories', api_views.CategoryViewSet, basename='api_categories')
router.register(r'api/products', api_views.ProductViewSet, basename='api_products')

urlpatterns = [
    path('', views.home_page, name='home'),
    path('products/', views.product_list, name='product_list'),
    path('product/<int:product_id>/', views.product_detail, name='product_detail'),
    path('cart/', views.cart_view, name='cart_view'),
    path('cart/clear/', views.clear_cart, name='clear_cart'),
    path('product/<int:product_id>/add-to-cart/', views.add_to_cart, name='add_to_cart'),
    path('toggle-theme/', views.toggle_theme, name='toggle_theme'),
    path('', include(router.urls)),
    path('chat/', views.chat_room, name='chat_room'),
]