from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import review_list, add_review, edit_review, delete_review
from . import api_views

app_name = 'reviews'

router = DefaultRouter()
router.register(r'api/reviews', api_views.ReviewViewSet, basename='api_reviews')

urlpatterns = [
    path('all/', review_list, name='review_list'),
    path('product/<int:product_id>/add/', add_review, name='add_review'),
    path('<int:review_id>/edit/', edit_review, name='edit_review'),
    path('<int:review_id>/delete/', delete_review, name='delete_review'),
    path('', include(router.urls)),
]