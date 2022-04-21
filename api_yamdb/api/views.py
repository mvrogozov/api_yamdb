from django.conf import settings
from django.core.mail import send_mail
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, status, viewsets
from rest_framework.decorators import action
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.tokens import RefreshToken

from reviews.models import Category, Genre, Review, Title
from users.models import User

from .api_mixins import ListCreateDestroyViewSet
from .api_permissions import AuthorOrReadOnly, IsAdmin, IsAdminOrReadOnly
from .filters import TitleFilter
from .serializers import (AuthSerializer, AuthTokenSerializer,
                          CategorySerializer, CommentSerializer,
                          GenreSerializer, ReviewSerializer,
                          TitleSerializerEdit, TitleSerializerSafe,
                          UserSerializer)


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'username'
    permission_classes = [IsAuthenticated & IsAdmin]
    pagination_class = LimitOffsetPagination
    filter_backends = (filters.SearchFilter,)
    search_fields = (
        'username',
        'first_name',
        'last_name',
        'role'
    )

    @action(
        detail=False,
        methods=['patch', 'get'],
        permission_classes=(IsAuthenticated,)
    )
    def me(self, request):
        user = get_object_or_404(User, username=request.user.username)
        if request.method == 'GET':
            serializer = UserSerializer(instance=user)
            return Response(serializer.data, status=status.HTTP_200_OK)

        serializer = UserSerializer(
            instance=user, data=request.data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        if request.user.is_superuser or request.user.is_admin:
            serializer.save()
        else:
            serializer.save(role=request.user.role)
        return Response(serializer.data, status=status.HTTP_200_OK)


class AuthView(APIView):
    def post(self, request):
        serializer = AuthSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        confirmation_code = urlsafe_base64_encode(
            force_bytes(serializer.validated_data.get('username'))
        )
        send_mail(
            'subj',
            confirmation_code,
            settings.ADMIN_EMAIL,
            [serializer.validated_data.get('email')],
            fail_silently=True,
        )
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


class AuthTokenView(APIView):
    def post(self, request):
        serializer = AuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.validated_data.get('username')
        user = get_object_or_404(User, username=username)
        right_code = urlsafe_base64_encode(force_bytes(username))
        if serializer.validated_data.get('confirmation_code') != right_code:
            return Response(
                serializer.validated_data, status=status.HTTP_400_BAD_REQUEST
            )

        refresh = RefreshToken.for_user(user)
        return Response(
            {'access': str(refresh.access_token)}, status=status.HTTP_200_OK
        )


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = [AuthorOrReadOnly]

    def get_queryset(self):
        title = get_object_or_404(Title, id=self.kwargs.get('title_id'))
        return title.reviews.all()

    def perform_create(self, serializer):
        title = get_object_or_404(Title, id=self.kwargs.get('title_id'))
        serializer.save(title=title, author=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [AuthorOrReadOnly]

    def get_queryset(self):
        review = get_object_or_404(Review, id=self.kwargs.get('review_id'))
        return review.comments.all()

    def perform_create(self, serializer):
        review = get_object_or_404(Review, id=self.kwargs.get('review_id'))
        serializer.save(review=review, author=self.request.user)


class CategoryViewSet(ListCreateDestroyViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = 'slug'
    filter_backends = (
        DjangoFilterBackend,
        filters.SearchFilter,
    )
    search_fields = ('name',)
    permission_classes = [IsAdminOrReadOnly]


class GenreViewSet(ListCreateDestroyViewSet):
    permission_classes = [IsAdminOrReadOnly]
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    lookup_field = 'slug'
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)


class TitleViewSet(viewsets.ModelViewSet):
    queryset = (
        Title.objects.all().annotate(
            rating=Avg('reviews__score')
        ).order_by('name')
    )
    filterset_class = TitleFilter
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [DjangoFilterBackend]

    def get_serializer_class(self):
        if self.action in ['post', 'create', 'partial_update']:
            return TitleSerializerEdit
        return TitleSerializerSafe
