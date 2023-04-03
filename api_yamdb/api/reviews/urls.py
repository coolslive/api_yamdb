from django.urls import include, path
from rest_framework.routers import DefaultRouter
from api.reviews.views import (
    CommentViewSet,
    ReviewViewSet,
    GenreViewSet,
    CategoryViewSet,
    TitleViewSet
)

app_name = 'reviews'

router_v1 = DefaultRouter()
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet,
    basename='comments'
)
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews',
    ReviewViewSet,
    basename='reviews'
)
router_v1.register(
    'genres',
    GenreViewSet,
    basename='genres'
)
router_v1.register(
    'categories',
    CategoryViewSet,
    basename='categories'
)
router_v1.register(
    'titles',
    TitleViewSet,
    basename='titles'
)

urlpatterns = [
    path('v1/', include(router_v1.urls)),
    path('', include(router_v1.urls))
]
