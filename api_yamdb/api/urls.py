from django.urls import path, include
from .views import AuthView, AuthTokenView, UserViewSet
from rest_framework import routers

API_VERSION = 'v1/'


router = routers.DefaultRouter()
router.register(r'users', UserViewSet, basename='api_users')

urlpatterns = [
    path(
        API_VERSION, include(router.urls)
    ),
    path(
        API_VERSION + 'auth/signup/',
        AuthView.as_view(),
        name='api_auth_signup'
    ),
    path(
        API_VERSION + 'auth/token/',
        AuthTokenView.as_view(),
        name='api_auth_token'
    ),
]
