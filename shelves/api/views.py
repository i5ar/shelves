from rest_framework import viewsets
from rest_framework.generics import ListAPIView

from rest_framework.permissions import (
    AllowAny,
    IsAuthenticated,
    IsAdminUser,
    IsAuthenticatedOrReadOnly)

from ..models import Customer
from .serializers import (
    # CustomerSerializer,
    CustomerHyperlinkedSerializer,
)


class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerHyperlinkedSerializer
    permission_classes = [AllowAny]

#
# class CustomerListAPIView(ListAPIView):
#     queryset = Customer.objects.all()
#     serializer_class = CustomerSerializer
