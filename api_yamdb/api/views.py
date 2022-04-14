from django.shortcuts import get_object_or_404

from rest_framework.generics import CreateAPIView
from reviews.models import User
from .serializers import AuthSerializer, AuthTokenSerializer, UserSerializer
from .api_permissions import IsAdmin
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.core.mail import send_mail
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.viewsets import ModelViewSet
from rest_framework import permissions

from rest_framework import viewsets, mixins

from reviews.models import Review, Title
from .serializers import ReviewSerializer, CommentSerializer


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'username'
    permission_classes = [IsAdmin]

    def retrieve(self, request, *args, **kwargs):
        print('vvv', request.META['PATH_INFO'])
        if request.META['PATH_INFO'].endswith(r'users/me/'):
            print('ddd')
        instance = get_object_or_404(User, pk=request.user.pk)
        print('\n\nbbb', type(instance))
        serializer = self.get_serializer(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)



class AuthView(APIView):

    def post(self, request):
        serializer = AuthSerializer(data=request.data)
        if serializer.is_valid():
            confirmation_code = urlsafe_base64_encode(
                force_bytes(serializer.validated_data.get('username'))
            )
            print('\n\naaaa', confirmation_code)
            send_mail(
                'subj',
                confirmation_code,
                'from@django.com',
                [serializer.validated_data.get('email')],
                fail_silently=True
            )
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AuthTokenView(APIView):

    def post(self, request):
        serializer = AuthTokenSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        username = serializer.data.get('username')
        user = get_object_or_404(User, username=username)
        right_code = urlsafe_base64_encode(
            force_bytes(username))
        if serializer.data.get('confirmation_code') != right_code:
            return Response(
                serializer.data,
                status=status.HTTP_400_BAD_REQUEST
            )

        refresh = RefreshToken.for_user(user)
        return Response(
            {'access': str(refresh.access_token)},
            status=status.HTTP_200_OK
        )
      
      
      
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
