from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from .models import User



class SignUpSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        max_length=254,
    )
    username = serializers.SlugField(
        max_length=150,
    )

    class Meta:
        fields = ("username", "email")
        model = User

    def validate(self, data):
        email = data['email']
        username = data['username']
        if username != 'me':
            if User.objects.filter(
                username=username
            ).exists() or User.objects.filter(email=email).exists():
                raise serializers.ValidationError(
                    'Пользователь с таким именем или email уже существует')
            return data
        raise serializers.ValidationError(
            'Недопустимое имя пользователя')


class ConfirmationCodeSerializer(serializers.Serializer):
    username = serializers.CharField(
        required=True
    )
    confirmation_code = serializers.CharField(required=True)