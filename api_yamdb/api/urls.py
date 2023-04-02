from rest_framework.routers import DefaultRouter

from django.urls import include, path

from api.views import (
    CategoryViewSet, CommentViewSet, GenreViewSet, ReviewViewSet, TitleViewSet,
)

app_name = "api"

router_v1 = DefaultRouter()
router_v1.register(
    r"titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments",
    CommentViewSet,
    basename="comments",
)
router_v1.register(
    r"titles/(?P<title_id>\d+)/reviews", ReviewViewSet, basename="reviews"
)
router_v1.register("genres", GenreViewSet, basename="genres")
router_v1.register("categories", CategoryViewSet, basename="categories")
router_v1.register("titles", TitleViewSet, basename="titles")

urlpatterns = [
    path("v1/", include(router_v1.urls)),
    path("", include(router_v1.urls)),
]
