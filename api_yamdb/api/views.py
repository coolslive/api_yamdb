from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from reviews.models import Review, Title
from api.serializers import ReviewSerializer, CommentSerializer
from api.permissions import IsAdminModeratorUser


class ReviewViewSet(viewsets.ModelViewSet):
    """Вьюсет для отзывов."""
    serializer_class = ReviewSerializer
    permission_classes = [IsAdminModeratorUser, ]

    def get_queryset(self):
        """Получает все отзывы к произведению."""
        title = get_object_or_404(Title, id=self.kwargs.get('title_id'))
        return title.reviews.all()

    def perform_create(self, serializer):
        """Создает новый отзыв."""
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Title, id=title_id)
        serializer.save(title=title, author=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    """Вьюсет для комментариев."""
    serializer_class = CommentSerializer
    permission_classes = [IsAdminModeratorUser, ]

    def get_queryset(self):
        """Получает все комментарии к отзыву."""
        review = get_object_or_404(Review, id=self.kwargs.get('review_id'))
        return review.comments.all()

    def perform_create(self, serializer):
        """Создает новый комментарий к отзыву."""
        review = get_object_or_404(Review, id=self.kwargs.get('review_id'))
        serializer.save(author=self.request.user, review=review)
