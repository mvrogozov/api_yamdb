from django.shortcuts import get_object_or_404
from rest_framework.generics import CreateAPIView
from reviews.models import User
from .serializers import AuthSerializer, AuthTokenSerializer
from .api_permissions import PostOnly
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.core.mail import send_mail
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.viewsets import ModelViewSet


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = AuthSerializer


class AuthView(CreateAPIView):

    queryset = User.objects.all()
    serializer_class = AuthSerializer

    def perform_create(self, serializer):
        confirmation_code = urlsafe_base64_encode(
            force_bytes(serializer.validated_data.get('username'))
        )
        print('\n\naaaa', confirmation_code)
        send_mail(
            'subj',
            confirmation_code,
            'from@django.com',
            ['to@pochta.com'],
            fail_silently=True
        )
        serializer.save()


class AuthTokenView(APIView):

    #permission_classes = [PostOnly]

    def post(self, request):
        serializer = AuthTokenSerializer(data=request.data)
        if serializer.is_valid():
            right_code = urlsafe_base64_encode(
                force_bytes(serializer.data.get('username')))
            
        if serializer.data.get('confirmation_code') != right_code:
            return Response(
                serializer.data,
                status=status.HTTP_400_BAD_REQUEST
            )
        user = get_object_or_404(User, username=serializer.data.get('username'))
        print('/n/n here ok ', user)
        refresh = RefreshToken.for_user(user)
        return Response({'access': str(refresh.access_token)}, status=status.HTTP_200_OK)
