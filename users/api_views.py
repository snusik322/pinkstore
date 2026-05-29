from rest_framework import generics, permissions
from users.models import Profile
from .serializers import ProfileSerializer
from drf_spectacular.utils import extend_schema


@extend_schema(
    summary = "Профиль текущего пользователя",
    description = (
        "Возвращает авторизованного пользователя:"
        "логин,email, телефон и адрес доставки. Требует аутентификации."
    ),
    
    tags = ['Пользователи']
)

class MyProfileAPIView(generics.RetrieveAPIView):
    serializer_class = ProfileSerializer
    permission_classes = [permissions.IsAuthenticated]
    def get_object(self):
        return Profile.objects.get(user = self.request.user)