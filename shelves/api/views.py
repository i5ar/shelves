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
    # queryset = Customer.objects.all()
    serializer_class = CustomerSerializer

    def get_queryset(self):
        """Filter the customers of the current user by the author."""
        return Customer.objects.filter(author=self.request.user)


class CustomerDetail(generics.RetrieveUpdateDestroyAPIView):
    # queryset = Customer.objects.all()
    serializer_class = CustomerSerializer

    def get_queryset(self):
        """Filter the customer of the current user by the author."""
        return Customer.objects.filter(author=self.request.user)


class ShelfList(generics.ListCreateAPIView):
    """List and create shelves.

    Front methods:
    - ``getShelves()``
    - ``postShelf()``
    """

    # queryset = Shelf.objects.all()
    serializer_class = ShelfListSerializer
    # permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def get_queryset(self):
        """Filter the shelves of the current user by the author."""
        return Shelf.objects.filter(author=self.request.user)


class ShelfDetail(generics.RetrieveUpdateDestroyAPIView):
    """Retrieve update and destroy shelf.

    Front methods:
    - ``getShelf()``
    - ``deleteShelf()``
    """

    # queryset = Shelf.objects.all()
    serializer_class = ShelfDetailSerializer
    # permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def get_queryset(self):
        """Filter the shelf of the current user by the author."""
        return Shelf.objects.filter(author=self.request.user)


class ContainerList(generics.ListAPIView):
    # queryset = Container.objects.all()
    serializer_class = ContainerSerializer
    # permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def get_queryset(self):
        """Filter the containers of the current user by the author of the
        shelf.
        """
        return Container.objects.filter(shelf__author=self.request.user)


class ContainerDetail(generics.RetrieveAPIView):
    # queryset = Container.objects.all()
    serializer_class = ContainerSerializer
    # permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def get_queryset(self):
        """Filter the container of the current user by the author of the
        shelf.
        """
        return Container.objects.filter(shelf__author=self.request.user)


class BinderList(generics.ListCreateAPIView):
    """List and create binders.

    Front methods:
    - ``postBinder()``
    - ``getBinders()``
    """

    # queryset = Binder.objects.all()
    serializer_class = BinderSerializer
    # permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def get_queryset(self):
        """Filter the binders of the current user by the author of the shelf of
        the container.
        """
        user = self.request.user
        return Binder.objects.filter(container__shelf__author=user)


class BinderDetail(generics.RetrieveUpdateDestroyAPIView):
    # queryset = Binder.objects.all()
    serializer_class = BinderSerializer
    # permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def get_queryset(self):
        """Filter the binder of the current user by the author of the shelf of
        the container.
        """
        user = self.request.user
        return Binder.objects.filter(container__shelf__author=user)


class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAdminUser,)


class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAdminUser,)
