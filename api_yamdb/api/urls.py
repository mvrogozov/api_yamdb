from django.urls import path, include
from .views import AuthView, AuthTokenView, UserViewSet
from .views import ReviewViewSet, CommentViewSet
from rest_framework import routers

API_VERSION = 'v1/'


router = routers.DefaultRouter()
router.register(r'users', UserViewSet, basename='api_users')
#router.register(r'users\/(?P<username>\w+)', SingleUserViewSet, basename='api_single_user')

router.register(
    'titles/(?P<title_id>\\d+)/reviews',
    ReviewViewSet,
    basename='reviews'
)

router.register(
    'titles/(?P<title_id>\\d+)/reviews/(?P<review_id>\\d+)/comments',
    CommentViewSet,
    basename='comments'
)


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
