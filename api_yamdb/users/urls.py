from django.urls import path , include
from rest_framework.routers import DefaultRouter
from users.views import signup, token


router_v1 = DefaultRouter()

urlpatterns = [
    path('', include(router_v1.urls)),
    path('auth/signup/', signup, name='signup'),
    path('auth/token/', token, name='token')
]