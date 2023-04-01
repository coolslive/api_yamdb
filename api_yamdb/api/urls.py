from django.urls import include, path
from rest_framework.routers import DefaultRouter
from api.views import CommentViewSet, ReviewViewSet

app_name = 'api'

v1_router = DefaultRouter()
v1_router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet
)
v1_router.register(
    r'titles/(?P<title_id>\d+)/reviews',
    ReviewViewSet
)

urlpatterns = [
    path('v1/', include(v1_router.urls)),
]
