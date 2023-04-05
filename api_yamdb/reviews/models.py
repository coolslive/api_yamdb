from django.core.validators import MinValueValidator
from django.db import models

from .validators import max_value_current_year

from users.models import User


class Category(models.Model):
    """Категории произведений."""
    name = models.CharField(
        max_length=256,
        verbose_name='Название категории'
    )
    slug = models.SlugField(
        unique=True,
        max_length=50,
        verbose_name='Слаг категории'
    )

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Genre(models.Model):
    """Жанры произведений."""
    name = models.CharField(
        max_length=256,
        verbose_name='Название категории'
    )
    slug = models.SlugField(
        unique=True,
        verbose_name='Слаг жанра'
    )

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'


class Title(models.Model):
    """Произведение искусства."""
    name = models.CharField(
        max_length=100,
        verbose_name='Название произведения'
    )
    year = models.PositiveSmallIntegerField(
        verbose_name='Год создания',
        validators=[
            MinValueValidator(0),
            max_value_current_year]
    )
    description = models.TextField(
        verbose_name='Описание произведения',
        blank=True,
    )
    genre = models.ManyToManyField(
        Genre,
        through='GenreConnect',
        related_name='genre',
        verbose_name='Жанр'
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        related_name='category',
        verbose_name='Категория',
    )

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'


class GenreConnect(models.Model):
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE
    )
    genre = models.ForeignKey(
        Genre,
        on_delete=models.CASCADE
    )

    def __str__(self) -> str:
        return self.genre


class Review(models.Model):
    """Класс отзывов."""
    text = models.TextField(
        verbose_name='Текст',
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Автор'
    )
    score = models.PositiveIntegerField(
        verbose_name='Oценка'
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата публикации',
        db_index=True
    )
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='произведение',
        null=True
    )

    class Meta:
        verbose_name = 'Отзыв'
        ordering = ('-pub_date',)
        constraints = (
            models.UniqueConstraint(
                fields=['author', 'title'],
                name='unique_author_title'
            ),
        )


class Comment(models.Model):
    """Класс комментариев."""
    text = models.TextField(
        verbose_name='Текст',
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Автор'
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата публикации',
        db_index=True,
    )
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='oтзыв',
    )

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ('-pub_date',)
