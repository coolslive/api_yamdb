from rest_framework import serializers

from django.forms import ValidationError
from django.shortcuts import get_object_or_404
from django.utils import timezone

from reviews.models import Category, Comment, Genre, Review, Title
from users.models import User


class CommentSerializer(serializers.ModelSerializer):
    """Сериалайзер для комментариев."""
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username',
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        fields = ('id', 'text', 'author', 'pub_date',)
        model = Comment


class GenreSerializer(serializers.ModelSerializer):
    """Сериалайзер для жанров."""
    class Meta:
        fields = ('name', 'slug')
        model = Genre


class CategorySerializer(serializers.ModelSerializer):
    """Сериалайзер для категорий."""
    class Meta:
        fields = ('name', 'slug')
        model = Category


class TitleSerializer(serializers.ModelSerializer):
    """Сериалайзер для произведений."""
    genre = GenreSerializer(many=True, read_only=True)
    category = CategorySerializer(read_only=True)
    rating = serializers.IntegerField()

    def get_rating(self, rating):
        return rating

    class Meta:
        fields = (
            'id', 'name', 'year', 'rating', 'description', 'genre', 'category')
        model = Title


class TitleCreateSerializer(serializers.ModelSerializer):
    """Сериалайзер для создания произведений."""
    category = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Category.objects.all()
    )
    genre = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Genre.objects.all(),
        many=True
    )

    class Meta:
        fields = (
            'id', 'name', 'year', 'description', 'genre', 'category')
        model = Title

        def validate_year(self, value):
            """
            Проверяет, что год указан в допустимых рамках.
            """
            year_now = timezone.now.year
            if value <= 0 or value > year_now:
                raise serializers.ValidationError(
                    'Год создания должен быть нашей эры и не больше текущего.'
                )
            return value


class ReviewSerializer(serializers.ModelSerializer):
    """Сериалайзер для отзывов."""
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )
    title = serializers.SlugRelatedField(
        slug_field='name',
        read_only=True
    )

    def validate(self, data):
        """
        Проверяет количество отзывов на произведение
        от одного пользователя.
        """
        request = self.context['request']
        title_id = self.context['view'].kwargs.get('title_id')
        title = get_object_or_404(Title, pk=title_id)
        if request.method == 'POST':
            if Review.objects.filter(
                    title=title,
                    author=request.user).exists():
                raise ValidationError(
                    'Вы уже оставляли отзыв к этому произведению!')
        return data

    def validate_score(self, score):
        """Проверяет, что оценка произведения в рамках допустимых значений."""
        if score < 1 or score > 10:
            raise serializers.ValidationError(
                'Рейтинг произведения должен быть от 1 до 10')
        return score

    class Meta:
        fields = ('id', 'text', 'author', 'score', 'pub_date', 'title')
        model = Review


class SignUpSerializer(serializers.ModelSerializer):
    """Сериализатор регистрации пользователей и выдачи токенов"""
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
    """Сериализатор получения JWT-токена"""
    username = serializers.CharField(
        required=True
    )
    confirmation_code = serializers.CharField(required=True)


class AdminSerializer(serializers.ModelSerializer):
    """Сериализатор для модели User.
    Права доступа: Администратор.
    """

    class Meta:
        fields = ("username", "email", "first_name",
                  "last_name", "bio", "role")
        model = User


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор для модели User.
    Права доступа: Любой авторизованный пользователь.
    """

    class Meta:
        fields = ("username", "email", "first_name",
                  "last_name", "bio", "role")
        model = User
        read_only_fields = ('role',)
