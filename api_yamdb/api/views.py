from functools import partial
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


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'username'
    permission_classes = [IsAdmin]

    def retrieve(self, request, *args, **kwargs):
        print('\n\nsss ', request.user)
        if request.META['PATH_INFO'].endswith(r'users/me/'):
            instance = get_object_or_404(User, pk=request.user.pk)
        else:
            instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def partial_update(self, request, *args, **kwargs):
        if request.META['PATH_INFO'].endswith(r'users/me/'):
            instance = get_object_or_404(User, pk=request.user.pk)
        else:
            instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
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
