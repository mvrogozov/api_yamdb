from django.conf import settings
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from rest_framework import filters, status
from rest_framework.decorators import action
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.tokens import RefreshToken

from api.api_permissions import IsAdmin
from .models import User
from .serializers import AuthSerializer, AuthTokenSerializer, UserSerializer


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
