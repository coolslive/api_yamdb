from django.urls import include, path

app_name = 'api'

urlpatterns = [
    path('', include('api.users.urls')),
    path('', include('api.reviews.urls')),
]
