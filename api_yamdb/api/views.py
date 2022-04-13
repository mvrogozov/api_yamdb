from django.shortcuts import get_object_or_404
from rest_framework import viewsets, mixins

from reviews.models import Review, Title
from .serializers import ReviewSerializer, CommentSerializer


class CreateMixin(mixins.CreateModelMixin, viewsets.GenericViewSet):
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class ReviewViewSet(CreateMixin, viewsets.ModelViewSet):
    serializer_class = ReviewSerializer

    def get_queryset(self):
        title = get_object_or_404(Title, id=self.kwargs.get('id'))
        return title.reviews.all()


class CommentViewSet(CreateMixin, viewsets.ModelViewSet):
    serializer_class = CommentSerializer

    def get_queryset(self):
        review = get_object_or_404(Review, id=self.kwargs.get('id'))
        return review.comments.all()
