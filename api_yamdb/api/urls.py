from django.urls import include, path
from rest_framework import routers

from .views import (AuthTokenView, AuthView, CategoryViewSet, CommentViewSet,
                    GenreViewSet, ReviewViewSet, TitleViewSet, UserViewSet)

API_VERSION = 'v1/'

router = routers.DefaultRouter()
router.register(r'users', UserViewSet, basename='api_users')
router.register('categories', CategoryViewSet, basename='category')
router.register('genres', GenreViewSet, basename='genre')
router.register(
    r'titles\/(?P<title_id>\d+)\/reviews', ReviewViewSet, basename='reviews'
)
router.register(
    r'titles\/(?P<title_id>\d+)\/reviews\/(?P<review_id>\d+)\/comments',
    CommentViewSet,
    basename='comments',
)
router.register('titles', TitleViewSet, basename='title')

urlpatterns = [
    path(API_VERSION, include(router.urls)),
    path(
        API_VERSION + 'auth/signup/',
        AuthView.as_view(),
        name='api_auth_signup',
    ),
    path(
        API_VERSION + 'auth/token/',
        AuthTokenView.as_view(),
        name='api_auth_token',
    ),
]
