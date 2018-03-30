import csv
import operator
from functools import reduce

from django.contrib.auth.models import User
from django.db.models import Q
from django.conf import settings
# from django.core.files.storage import default_storage
from django.db import IntegrityError
from django.utils.translation import ugettext as _

from rest_framework import generics, status
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
    UploadSerializer,
    AttachmentSerializer,
    BinderSerializer
)

from ..models import (
    Customer,
    Shelf,
    Binder,
    # Upload,
    Attachment,
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
            'shelves-api:uploads-api', request=request, format=format),
        'attachments': reverse(
            'shelves-api:attachments-api', request=request, format=format)
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

    # https://stackoverflow.com/questions/45532965/
    # http://www.django-rest-framework.org/api-guide/generic-views/#mixins
    # http://www.django-rest-framework.org/tutorial/3-class-based-views/#using-mixins
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        data = serializer.data

        try:
            # Get binders by shelf code
            binders = Binder.objects.filter(shelf__code=data.get('code'))
            cols = data.get('cols')
            rows = data.get('rows')

            cells = []
            for i in range(cols):
                for j in range(rows):
                    cells.append({'col': i+1, 'row': j+1, 'binders': []})

            for i, cell in enumerate(cells):
                for b in binders:
                    if b.col == cell.get('col') and b.row == cell.get('row'):
                        cells[i]['binders'].append({
                            'id': b.id,
                            'col': b.col,
                            'row': b.row,
                            'title': b.title,
                            'content': b.content,
                            'updated': b.updated,
                            'customer': {
                                'id': b.customer.id,
                                'name': b.customer.name,
                                'code': b.customer.code,
                                'note': b.customer.note,
                            } if b.customer else None,
                        })

        except Binder.DoesNotExist:
            cells = None
        data['cells'] = cells
        return Response(data)

    def get_queryset(self):
        """Filter the shelf of the current user by the author."""
        if settings.DEBUG_USER_ID:
            return Shelf.objects.filter(author=User.objects.get(
                id=settings.DEBUG_USER_ID))
        return Shelf.objects.filter(author=self.request.user)


class BinderListCreate(generics.ListCreateAPIView):
    serializer_class = BinderSerializer
    if settings.DEBUG_USER_ID:
        permission_classes = (permissions.AllowAny,)
    else:
        permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        if settings.DEBUG_USER_ID:
            user = User.objects.get(id=settings.DEBUG_USER_ID)
        else:
            user = self.request.user
        queryset = Binder.objects.filter(shelf__author=user)

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

    # https://stackoverflow.com/questions/35501137/
    def create(self, request, *args, **kwargs):
        """Nest customer fields in the response."""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        data = serializer.data
        try:
            c = Customer.objects.get(id=data.get('customer'))
            customer = {
                'id': c.id,
                'name': c.name,
                'code': c.code,
                'note': c.note
            }
            print(customer)
        except Customer.DoesNotExist:
            customer = None
        data['customer'] = customer
        return Response(
            data,
            status=status.HTTP_201_CREATED,
            headers=self.get_success_headers(data)
        )


class BinderRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = BinderSerializer
    if settings.DEBUG_USER_ID:
        permission_classes = (permissions.AllowAny,)
    else:
        permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        if settings.DEBUG_USER_ID:
            user = User.objects.get(id=settings.DEBUG_USER_ID)
        else:
            user = self.request.user
        return Binder.objects.filter(shelf__author=user)

    # https://stackoverflow.com/questions/39083414/
    def retrieve(self, request, *args, **kwargs):
        """Nest customer fields in the response."""
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        data = serializer.data
        try:
            c = Customer.objects.get(id=data.get('customer'))
            customer = {
                'id': c.id,
                'name': c.name,
                'code': c.code,
                'note': c.note
            }
            # NOTE: Get all the fields.
            # for f in c._meta.get_fields():
            #     a = getattr(c, f.name)
            #     customer[f.name] = int(a) if (type(a) == int) else str(a)
        except Customer.DoesNotExist:
            customer = None
        data['customer'] = customer
        return Response(data)

    def update(self, request, *args, **kwargs):
        """Nest customer fields in the response."""
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        data = serializer.data
        try:
            c = Customer.objects.get(id=data.get('customer'))
            customer = {
                'id': c.id,
                'name': c.name,
                'code': c.code,
                'note': c.note
            }
        except Customer.DoesNotExist:
            customer = None
        data['customer'] = customer
        return Response(data)


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
    NOTE: Use only `Authorization` header in the request.

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

            if settings.DEBUG_USER_ID:
                user = User.objects.get(id=settings.DEBUG_USER_ID)
            else:
                user = self.request.user

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
                    for row in reader:
                        try:
                            Customer.objects.get_or_create(
                                name=row['name'],
                                code=row['code'],
                                note=row['note'],
                                author=user
                            )
                        except TypeError as e:
                            raise ValidationError(e, code='auth')
                        except IntegrityError as e:
                            """
                            An integrity error may happen if two customers have
                            the same code.
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
                                    author=user
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


class AttachmentListCreate(generics.ListCreateAPIView):
    # parser_classes = (MultiPartParser, FormParser)

    serializer_class = AttachmentSerializer
    if settings.DEBUG_USER_ID:
        permission_classes = (permissions.AllowAny,)
    else:
        permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        if settings.DEBUG_USER_ID:
            user = User.objects.get(id=settings.DEBUG_USER_ID)
        else:
            user = self.request.user
        return Attachment.objects.filter(binder__shelf__author=user)


class AttachmentRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    # parser_classes = (MultiPartParser, FormParser)

    serializer_class = AttachmentSerializer
    if settings.DEBUG_USER_ID:
        permission_classes = (permissions.AllowAny,)
    else:
        permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        if settings.DEBUG_USER_ID:
            user = User.objects.get(id=settings.DEBUG_USER_ID)
        else:
            user = self.request.user
        return Attachment.objects.filter(binder__shelf__author=user)

    def update(self, request, *args, **kwargs):
        """Use a ``partial`` update (PATCH) for the title and the binder id.

        A new file would be otherwise required each time.

        """
        instance = self.get_object()
        # Partial update
        # https://stackoverflow.com/questions/27980390/
        serializer = self.get_serializer(
            instance,
            data=request.data,
            partial=True
        )
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)
