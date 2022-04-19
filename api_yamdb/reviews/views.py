from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, mixins, viewsets


from api.api_permissions import IsAdmin, ReadOnly, AuthorOrReadOnly
from api.filters import TitleFilter

from .models import Category, Genre, Review, Title
from .serializers import (CategorySerializer, CommentSerializer,
                          GenreSerializer, ReviewSerializer,
                          TitleSerializerEdit, TitleSerializerSafe)


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = [AuthorOrReadOnly]

    def get_queryset(self):
        title = get_object_or_404(Title, id=self.kwargs.get("title_id"))
        return title.reviews.all()

    def perform_create(self, serializer):
        title = get_object_or_404(Title, id=self.kwargs.get("title_id"))
        serializer.save(title=title, author=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [AuthorOrReadOnly]

    def get_queryset(self):
        review = get_object_or_404(Review, id=self.kwargs.get("review_id"))
        return review.comments.all()

    def perform_create(self, serializer):
        review = get_object_or_404(Review, id=self.kwargs.get("review_id"))
        serializer.save(review=review, author=self.request.user)


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
    permission_classes = [IsAdmin]

    def get_permissions(self):
        if self.action == "list":
            return (ReadOnly(),)
        return super().get_permissions()


class GenreViewSet(ListCreateDestroyViewSet):
    permission_classes = [IsAdmin]
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    lookup_field = "slug"
    filter_backends = (filters.SearchFilter,)
    search_fields = ("name",)

    def get_permissions(self):
        if self.action == "list":
            return (ReadOnly(),)
        return super().get_permissions()


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    filterset_class = TitleFilter
    permission_classes = [IsAdmin]
    filter_backends = [DjangoFilterBackend]

    def get_permissions(self):
        if self.action in ["list", "retrieve"]:
            return (ReadOnly(),)
        return super().get_permissions()

    def get_serializer_class(self):
        if self.action in ["post", "create", "partial_update"]:
            return TitleSerializerEdit
        return TitleSerializerSafe
