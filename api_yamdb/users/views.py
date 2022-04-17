from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from rest_framework import filters, status
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, mixins, status, viewsets
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import (
    IsAuthenticated,
    IsAuthenticatedOrReadOnly,
)
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.tokens import RefreshToken

from .models import User

from .api_permissions import IsAdmin
from .serializers import AuthSerializer, AuthTokenSerializer, UserSerializer
from .models import Category, Genre, Review, Title

from .api_permissions import IsAdmin
from .serializers import (
    AuthSerializer,
    AuthTokenSerializer,
    CategorySerializer,
    CommentSerializer,
    GenreSerializer,
    ReviewSerializer,
    TitleSerializer,
    UserSerializer,
)


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


class MeView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        user = get_object_or_404(User, username=request.user.username)
        serializer = UserSerializer(instance=user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request):
        user = get_object_or_404(User, username=request.user.username)
        serializer = UserSerializer(
            instance=user, data=request.data, partial=True
        )
        if serializer.is_valid():
            if request.user.is_superuser or request.user.role == 'admin':
                serializer.save()
            else:
                serializer.save(role=request.user.role)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AuthView(APIView):
    def post(self, request):
        serializer = AuthSerializer(data=request.data)
        if serializer.is_valid():
            confirmation_code = urlsafe_base64_encode(
                force_bytes(serializer.validated_data.get("username"))
            )
            send_mail(
                "subj",
                confirmation_code,
                "from@django.com",
                [serializer.validated_data.get("email")],
                fail_silently=True,
            )
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AuthTokenView(APIView):
    def post(self, request):
        serializer = AuthTokenSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST
            )
        username = serializer.data.get('username')
        user = get_object_or_404(User, username=username)
        right_code = urlsafe_base64_encode(force_bytes(username))
        if serializer.data.get("confirmation_code") != right_code:
            return Response(
                serializer.data, status=status.HTTP_400_BAD_REQUEST
            )

        refresh = RefreshToken.for_user(user)
        return Response(
            {"access": str(refresh.access_token)}, status=status.HTTP_200_OK
        )


class CreateMixin(mixins.CreateModelMixin, viewsets.GenericViewSet):
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class ReviewViewSet(CreateMixin, viewsets.ModelViewSet):
    serializer_class = ReviewSerializer

    def get_queryset(self):
        title = get_object_or_404(Title, id=self.kwargs.get("id"))
        return title.reviews.all()


class CommentViewSet(CreateMixin, viewsets.ModelViewSet):
    serializer_class = CommentSerializer

    def get_queryset(self):
        review = get_object_or_404(Review, id=self.kwargs.get("id"))
        return review.comments.all()


class ListCreateDestroyViewSet(
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet,
):

    pass


class CategoryViewSet(ListCreateDestroyViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = "slug"
    filter_backends = (
        DjangoFilterBackend,
        filters.SearchFilter,
    )
    search_fields = ("name",)
    permission_classes = [IsAuthenticatedOrReadOnly, IsAdmin]


class GenreViewSet(ListCreateDestroyViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly, IsAdmin]
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    lookup_field = "slug"
    filter_backends = (filters.SearchFilter,)
    search_fields = ("name",)


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
