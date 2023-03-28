from django.core.mail import send_mail
from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken

from .serializers import SignUpSerializer, ConfirmationCodeSerializer
from .models import User


@api_view(["POST"])
@permission_classes([AllowAny])
def signup(request):
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
            subject="YaMDb registration",
            message=f"Your confirmation code: {confirmation_code}",
            from_email=None,
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
            subject="YaMDb registration",
            message=f"Your confirmation code: {confirmation_code}",
            from_email=None,
            recipient_list=[user.email],
            )
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
@permission_classes([AllowAny])
def token(request):
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
    pass
