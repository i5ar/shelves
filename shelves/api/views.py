from django.contrib.auth.models import User

# from rest_framework.generics import ListAPIView
# from rest_framework.permissions import (
#     AllowAny,
#     IsAuthenticated,
#     IsAdminUser,
#     IsAuthenticatedOrReadOnly)
# from rest_framework import viewsets

from ..models import (
    Customer,
    RegularBin,
    RegularShelf,
    Binder,
)
from .serializers import (
    CustomerSerializer,
    RegularShelfSerializer,
    UserSerializer,
    # CustomerHyperlinkedSerializer,
    # RegularBinHyperlinkedSerializer,
    # RegularShelfHyperlinkedSerializer,
    # BinderHyperlinkedSerializer,
)


# class CustomerListAPIView(ListAPIView):
#     queryset = Customer.objects.all()
#     serializer_class = CustomerSerializer


# class CustomerViewSet(viewsets.ModelViewSet):
#     queryset = Customer.objects.all()
#     serializer_class = CustomerHyperlinkedSerializer
#     permission_classes = [IsAuthenticatedOrReadOnly]


# class RegularBinViewSet(viewsets.ModelViewSet):
#     queryset = RegularBin.objects.all()
#     serializer_class = RegularBinHyperlinkedSerializer
#     permission_classes = [IsAuthenticatedOrReadOnly]


# class RegularShelfViewSet(viewsets.ModelViewSet):
#     queryset = RegularShelf.objects.all()
#     serializer_class = RegularShelfHyperlinkedSerializer
#     permission_classes = [IsAuthenticatedOrReadOnly]


# class BinderViewSet(viewsets.ModelViewSet):
#     queryset = Binder.objects.all()
#     serializer_class = BinderHyperlinkedSerializer
#     permission_classes = [IsAuthenticatedOrReadOnly]


from rest_framework import generics
from rest_framework import permissions
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework import renderers


@api_view(['GET'])
def shelves_root(request, format=None):
    return Response({
        'customers': reverse(
            'shelves-api:customer-list', request=request, format=format),
        'shelves': reverse(
            'shelves-api:regularshelf-list', request=request, format=format),
        'users': reverse(
            'shelves-api:user-list', request=request, format=format)
    })


class RegularShelfList(generics.ListCreateAPIView):
    queryset = RegularShelf.objects.all()
    serializer_class = RegularShelfSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    # def perform_create(self, serializer):
    #     serializer.save(owner=self.request.user)


class RegularShelfDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = RegularShelf.objects.all()
    serializer_class = RegularShelfSerializer
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,)


class CustomerList(generics.ListCreateAPIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer


class CustomerDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer


class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
