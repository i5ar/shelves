# from django.contrib.auth.models import User
from django.contrib.auth import get_user_model

from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from rest_framework.views import APIView

from rest_framework import generics
from rest_framework import permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.reverse import reverse

from .serializers import (
    UserSerializer,
    UserCreateSerializer,
    UserLoginSerializer,
    MemberSerializer,
    MemberCreateSerializer
)

from ..models import Member

User = get_user_model()


@api_view(['GET'])
@permission_classes((permissions.AllowAny,))
def accounts_root(request, format=None):
    return Response({
        'users': reverse(
            'accounts-api:user-list', request=request, format=format),
        'members': reverse(
            'accounts-api:member-list', request=request, format=format),
        'register': reverse(
            'accounts-api:register', request=request, format=format),
    })


class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAdminUser,)


class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAdminUser,)


class MemberList(generics.ListAPIView):
    queryset = Member.objects.all()
    serializer_class = MemberSerializer
    permission_classes = (permissions.IsAdminUser,)


class MemberDetail(generics.RetrieveAPIView):
    queryset = Member.objects.all()
    serializer_class = MemberSerializer
    permission_classes = (permissions.IsAdminUser,)


class MemberCreateAPIView(generics.CreateAPIView):
    serializer_class = MemberCreateSerializer
    queryset = Member.objects.all()
    permission_classes = [permissions.AllowAny]


class UserLoginAPIView(APIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = UserLoginSerializer

    def post(self, request, *args, **kwargs):
        data = request.data
        serializer = UserLoginSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            new_data = serializer.data
            return Response(new_data, status=HTTP_200_OK)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)
