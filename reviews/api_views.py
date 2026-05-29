from rest_framework import viewsets, permissions
from reviews.models import Review
from .serializers import ReviewSerializer
from drf_spectacular.utils import extend_schema, extend_schema_view

@extend_schema_view(
    list=extend_schema(summary="Список отзывов", tags=['Отзывы']),
    retrieve=extend_schema(summary="Детали отзыва", tags=['Отзывы']),
    create=extend_schema(summary="Создать отзыв", tags=['Отзывы']),
    update=extend_schema(summary="Обновить отзыв", tags=['Отзывы']),
    partial_update=extend_schema(summary="Частично обновить отзыв", tags=['Отзывы']),
    destroy=extend_schema(summary="Удалить отзыв", tags=['Отзывы']),
)
class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)