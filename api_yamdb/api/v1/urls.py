from rest_framework.routers import DefaultRouter

from django.urls import include, path

from .views import (
    CategoryViewSet, CommentViewSet, GenreViewSet, ReviewViewSet, TitleViewSet,
    UserViewSet, signup, token,
)

app_name = 'api.v1'

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
router_v1.register(
    'users',
    UserViewSet,
    basename='users'
)

urlpatterns = [
    path('', include(router_v1.urls)),
    path('v1/', include(router_v1.urls)),
    path('auth/signup/', signup, name='signup'),
    path('auth/token/', token, name='token')
]
