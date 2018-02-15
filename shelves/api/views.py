import csv
import operator
from functools import reduce

from django.contrib.auth.models import User
from django.db.models import Q
from django.conf import settings
# from django.core.files.storage import default_storage
from django.db import IntegrityError
from django.utils.translation import ugettext as _

from rest_framework import generics, viewsets
from rest_framework import permissions
from rest_framework.serializers import ValidationError
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.reverse import reverse
from rest_framework.parsers import (
    FormParser,
    MultiPartParser,
)

from .serializers import (
    UserSerializer,
    CustomerSerializer,
    ShelfListCreateSerializer,
    ShelfRetrieveUpdateDestroySerializer,
    BinderListRetrieveSerializer,
    BinderCreateUpdateDestroySerializer,
    UploadSerializer,
)

from ..models import (
    Customer,
    Shelf,
    Binder,
    Upload,
)


@api_view(['GET'])
def shelves_root(request, format=None):
    return Response({
        'users': reverse(
            'shelves-api:users-api', request=request, format=format),
        'customers': reverse(
            'shelves-api:customers-api', request=request, format=format),
        'binders': reverse(
            'shelves-api:binders-api', request=request, format=format),
        'shelves': reverse(
            'shelves-api:shelves-api', request=request, format=format),
        'uploads': reverse(
            'shelves-api:uploads-api', request=request, format=format)
    })


class CustomerListCreate(generics.ListCreateAPIView):
    # queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    if settings.DEBUG_USER_ID:
        permission_classes = (permissions.AllowAny,)
    else:
        permission_classes = (permissions.IsAuthenticated,)

    def perform_create(self, serializer):
        if settings.DEBUG_USER_ID:
            serializer.save(author=User.objects.get(id=settings.DEBUG_USER_ID))
        else:
            serializer.save(author=self.request.user)

    def get_queryset(self):
        """Filter the customers of the current user by the author."""
        if settings.DEBUG_USER_ID:
            return Customer.objects.filter(
                author=User.objects.get(id=settings.DEBUG_USER_ID))
        return Customer.objects.filter(author=self.request.user)


class CustomerRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    # queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    lookup_field = 'code'
    if settings.DEBUG_USER_ID:
        permission_classes = (permissions.AllowAny,)
    else:
        permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        """Filter the customer of the current user by the author."""
        if settings.DEBUG_USER_ID:
            return Customer.objects.filter(
                author=User.objects.get(id=settings.DEBUG_USER_ID))
        return Customer.objects.filter(author=self.request.user)


class ShelfListCreate(generics.ListCreateAPIView):
    """List and create shelves.

    Front methods:
    - ``getShelves()``
    - ``postShelf()``
    """

    # queryset = Shelf.objects.all()
    serializer_class = ShelfListCreateSerializer
    if settings.DEBUG_USER_ID:
        permission_classes = (permissions.AllowAny,)
    else:
        permission_classes = (permissions.IsAuthenticated,)

    def perform_create(self, serializer):
        if settings.DEBUG_USER_ID:
            serializer.save(author=User.objects.get(id=settings.DEBUG_USER_ID))
        else:
            serializer.save(author=self.request.user)

    def get_queryset(self):
        """Filter the shelves of the current user by the author."""
        if settings.DEBUG_USER_ID:
            return Shelf.objects.filter(author=User.objects.get(
                id=settings.DEBUG_USER_ID))
        return Shelf.objects.filter(author=self.request.user)


class ShelfRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    """Retrieve update and destroy shelf.

    Front methods:
    - ``getShelf()``
    - ``deleteShelf()``
    """

    lookup_field = 'code'
    # queryset = Shelf.objects.all()
    serializer_class = ShelfRetrieveUpdateDestroySerializer
    if settings.DEBUG_USER_ID:
        permission_classes = (permissions.AllowAny,)
    else:
        permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        """Filter the shelf of the current user by the author."""
        if settings.DEBUG_USER_ID:
            return Shelf.objects.filter(author=User.objects.get(
                id=settings.DEBUG_USER_ID))
        return Shelf.objects.filter(author=self.request.user)


class BinderViewSet(viewsets.ModelViewSet):
    """Binder view set based on different serializers."""

    # queryset = Binder.objects.all()
    # serializer_class = BinderSerializer
    if settings.DEBUG_USER_ID:
        permission_classes = (permissions.AllowAny,)
    else:
        permission_classes = (permissions.IsAuthenticated,)

    def get_serializer_class(self):
        if self.action == 'list' or self.action == 'retrieve':
            return BinderListRetrieveSerializer
        else:
            return BinderCreateUpdateDestroySerializer

    def get_queryset(self):
        """
        Filter the binders of the current user by the author of the shelf of
        the container.
        Filter the binders against query parameters.
        """

        # NOTE: Debug the action.
        # http://www.django-rest-framework.org/api-guide/viewsets/#viewset-actions
        # print('\033[1m' 'DEBUG', end=' ')
        # print(self.action)
        # print('\033[0m')

        if settings.DEBUG_USER_ID:
            user = User.objects.get(id=settings.DEBUG_USER_ID)
        else:
            user = self.request.user
        queryset = Binder.objects.filter(shelf__author=user)

        if self.action == 'list':
            # Filtering against query parameters
            # http://www.django-rest-framework.org/api-guide/filtering/#filtering-against-query-parameters
            query = self.request.query_params.get('q', None)
            if query is not None:
                query_list = query.split()
                # TODO: DRY because of ``BinderListView`` queryset.
                queryset = queryset.filter(
                    reduce(
                        operator.and_,
                        (Q(title__icontains=q) for q in query_list)
                    ) | reduce(
                        operator.and_,
                        (Q(content__icontains=q) for q in query_list)
                    ) | reduce(
                        operator.and_,
                        (Q(customer__code__icontains=q) for q in query_list)
                    ) | reduce(
                        operator.and_,
                        (Q(customer__name__icontains=q) for q in query_list)
                    )
                )

        return queryset


class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAdminUser,)


class UserRetrieve(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAdminUser,)


# Using ModelViewSet and Dropbox
# https://stackoverflow.com/questions/37987188/
# Using APIView
# https://stackoverflow.com/questions/39887923/
class UploadView(APIView):
    """
    NOTE: Use only `Authorization` header in Postman.

    """
    parser_classes = (MultiPartParser, FormParser)
    serializer_class = UploadSerializer

    if settings.DEBUG_USER_ID:
        permission_classes = (permissions.AllowAny,)
    else:
        permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, format=None):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            # Save CSV file
            # upload = Upload(**serializer.validated_data)
            # upload.save()

            # Import CSV data im memory
            # https://www.reddit.com/r/django/comments/2grsay/how_to_read_csv_file_from_memory/
            import io

            csv_file = self.request.data.get('csv_file')
            # with open(default_storage.path(upload.csv_file)) as f:
            with io.StringIO(csv_file.read().decode('utf-8')) as f:
                has_header = csv.Sniffer().has_header(f.read(1024))
                f.seek(0)
                if has_header:
                    reader = csv.DictReader(f)
                    print(f)
                    for row in reader:
                        try:
                            Customer.objects.get_or_create(
                                name=row['name'],
                                code=row['code'],
                                note=row['note'],
                                author=self.request.user
                            )
                        except TypeError as e:
                            raise ValidationError(e, code='auth')
                        except IntegrityError as e:
                            """
                            An integrity error may happen if two customers have the
                            same code.
                            """
                            # print('{0!r}'.format(e))
                            raise ValidationError(e, code='integrity')
                        except KeyError as e:
                            """
                            Key error may happen if CSV header is divergent
                            from model fields
                            """
                            try:
                                """
                                Pretend internationalized field name match the
                                CSV header
                                """
                                Customer.objects.get_or_create(
                                    name=row[_('name')],
                                    code=row[_('code')],
                                    note=row[_('note')],
                                    author=self.request.user
                                )
                            except KeyError as e:
                                raise ValidationError(
                                    'Is the field {} present in the CSV file '
                                    'header?'.format(e),
                                    code='key'
                                )

                else:
                    raise ValidationError(
                        _(
                            'The CSV file require a proper header in order.'
                            'Be sure to provide an id field.'
                        ), code='invalid'
                    )

            return Response({'success': 'Imported successfully'})
        else:
            return Response(serializer.errors, status=400)
