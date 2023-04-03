from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.filters import SearchFilter
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken

from .models import User
from .permissions import IsAdmin
from .serializers import (AdminSerializer, ConfirmationCodeSerializer,
                          SignUpSerializer, UserSerializer)


@api_view(["POST"])
@permission_classes([AllowAny])
def signup(request):
    """Получение кода подтверждения на email"""
    serializer = SignUpSerializer(data=request.data)
    username = request.data.get('username')
    email = request.data.get('email')
    try:
        user = User.objects.get(username=username, email=email)
    except Exception:
        user = None
    if user:
        confirmation_code = default_token_generator.make_token(user)
        send_mail(
            subject="Регистрация YaMDb",
            message=(
                f'Код подтверждения для {user.username}:{confirmation_code}.'
            ),

            recipient_list=[user.email],
        )
        message = ('Данный пользователь уже зарегистрирован.'
                   'Сообщение с кодом отправлено на почту.')
        return Response(message, status=status.HTTP_200_OK)
    if serializer.is_valid(raise_exception=True):
        serializer.save()
        username = serializer.validated_data["username"]
        user = get_object_or_404(User, username=username)
        confirmation_code = default_token_generator.make_token(user)
        send_mail(
            subject="Регистрация YaMDb",
            message=(
                f'Код подтверждения для {user.username}:{confirmation_code}.'
            ),
            from_email=None,
            recipient_list=[user.email],
        )
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
@permission_classes([AllowAny])
def token(request):
    """Получение JWT-токена."""
    serializer = ConfirmationCodeSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = get_object_or_404(
        User,
        username=serializer.validated_data["username"]
    )

    if default_token_generator.check_token(
        user, serializer.validated_data["confirmation_code"]
    ):
        token = AccessToken.for_user(user)
        return Response({"token": str(token)}, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserViewSet(viewsets.ModelViewSet):
    """Получение всех пользователей, добавление пользователя администратором.
    Получение, изменение и удаление пользователя по username администратором.
    Получение и изменение данных своей учетной записи пользователем.
    """
    queryset = User.objects.all()
    serializer_class = AdminSerializer
    permission_classes = (IsAdmin, )
    filter_backends = (SearchFilter,)
    search_fields = ['username', ]
    lookup_field = 'username'
    http_method_names = ['get', 'post', 'patch', 'delete', 'head']

    @action(
        url_path='me',
        methods=['get', 'patch'],
        detail=False,
        permission_classes=(IsAuthenticated,)
    )
    def show_user_profile(self, request):
        if request.method == "GET":
            serializer = UserSerializer(request.user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        if request.method == "PATCH":
            serializer = UserSerializer(
                request.user,
                data=request.data,
                partial=True
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
