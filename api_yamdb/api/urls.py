from django.urls import include, path
from rest_framework import routers

from users.views import AuthTokenView, AuthView, MeView, UserViewSet
from users.views import (
    CategoryViewSet, CommentViewSet, GenreViewSet, ReviewViewSet, TitleViewSet,
)

API_VERSION = 'v1/'

router = routers.DefaultRouter()
router.register(r"users", UserViewSet, basename="api_users")
router.register("categories", CategoryViewSet, basename="category")
router.register("genres", GenreViewSet, basename="genre")
router.register("titles", TitleViewSet, basename="title")
router.register(
    "titles/(?P<title_id>\\d+)/reviews", ReviewViewSet, basename="reviews"
)
router.register(
    "titles/(?P<title_id>\\d+)/reviews/(?P<review_id>\\d+)/comments",
    CommentViewSet,
    basename="comments",
)


urlpatterns = [
    path(API_VERSION + "users/me/", MeView.as_view(), name="api_users_me"),
    path(API_VERSION, include(router.urls)),
    path(
        API_VERSION + 'auth/signup/',
        AuthView.as_view(),
        name="api_auth_signup",
    ),
    path(
        API_VERSION + "auth/token/",
        AuthTokenView.as_view(),
        name="api_auth_token",
    ),
]
