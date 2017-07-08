from django.contrib.auth.models import User

from rest_framework import generics
from rest_framework import permissions
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse

from .serializers import (
    CustomerSerializer,
    ShelfListSerializer,
    ShelfDetailSerializer,
    ContainerSerializer,
    BinderSerializer,
    UserSerializer,
)

from ..models import (
    Customer,
    Shelf,
    Container,
    Binder,
)


@api_view(['GET'])
def shelves_root(request, format=None):
    return Response({
        'users': reverse(
            'shelves-api:user-list', request=request, format=format),
        'customers': reverse(
            'shelves-api:customer-list', request=request, format=format),
        'binders': reverse(
            'shelves-api:binder-list', request=request, format=format),
        'containers': reverse(
            'shelves-api:container-list', request=request, format=format),
        'shelves': reverse(
            'shelves-api:shelf-list', request=request, format=format),
    })


class CustomerList(generics.ListCreateAPIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer


class CustomerDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer


class ShelfList(generics.ListCreateAPIView):
    queryset = Shelf.objects.all()
    serializer_class = ShelfListSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    # def perform_create(self, serializer):
    #     serializer.save(owner=self.request.user)


class ShelfDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Shelf.objects.all()
    serializer_class = ShelfDetailSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)


class ContainerList(generics.ListAPIView):
    queryset = Container.objects.all()
    serializer_class = ContainerSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)


class ContainerDetail(generics.RetrieveAPIView):
    queryset = Container.objects.all()
    serializer_class = ContainerSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)


class BinderList(generics.ListCreateAPIView):
    queryset = Binder.objects.all()
    serializer_class = BinderSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)


class BinderDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Binder.objects.all()
    serializer_class = BinderSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)


class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
