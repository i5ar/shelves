from rest_framework import viewsets

from rest_framework.permissions import (
    AllowAny,
    IsAuthenticated,
    IsAdminUser,
    IsAuthenticatedOrReadOnly)

from .serializers import CustomerSerializer
from ..models import Customer

# ViewSets define the view behavior.
class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer

    # TODO: Change to permission
    permission_classes = [AllowAny]
    