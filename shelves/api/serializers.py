from django.contrib.auth.models import User
from django.conf import settings
from django.core.exceptions import ValidationError

from rest_framework import serializers

import os
import logging
from collections import OrderedDict

from ..models import (
    Customer,
    Container,
    Shelf,
    Binder,
)

# NOTE: Logging configuration used by the debug window in `startsession.sh`.
logging.basicConfig(
    filename = os.path.join(settings.BASE_DIR, 'api.log'),
    level = logging.DEBUG if settings.DEBUG else logging.WARNING,
    format = "%(levelname)s %(asctime)s %(message)s",
    filemode = "w"  # Run `tail` with `-vn +1` option to output all the rows
)


class UserSerializer(serializers.HyperlinkedModelSerializer):

    # NOTE: Uncomment if User is also Customer
    # customer = serializers.HyperlinkedRelatedField(
    #     view_name='shelves-api:customer-detail', read_only=True)

    class Meta:
        model = User
        # NOTE: Add `customer` field if User is also Customer
        fields = ('url', 'id', 'username')  # previusly `customer`
        extra_kwargs = {
            'url': {'view_name': "shelves-api:user-detail"},
        }


class CustomerSerializer(serializers.HyperlinkedModelSerializer):

    '''
    # NOTE: Tricky for further development of the API.
    user = serializers.CharField()

    def create(self, validated_data):
        """Create a new customer.

        The `user` field as defined above is a username, so it must be
        converted in a User object
        """
        username = validated_data.get('user')
        user = User.objects.get(username=username)
        validated_data['user'] = user
        return Customer.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """Update a new customer.

        The `user` field as defined above is a username, so it must be
        converted in a User object
        """
        username = validated_data.get('user')
        instance.user = User.objects.get(username=username)
        instance.code = validated_data.get('code', instance.code)
        instance.save()
        return instance
    '''

    class Meta:
        model = Customer
        # NOTE: The author is created from the generic view.
        fields = (
            # 'author',
            'url',
            'id',
            'name',  # `name` previusly `user`
            'code'
        )
        extra_kwargs = {
            'url': {'view_name': "shelves-api:customer-detail"},
            # 'author': {'view_name': "shelves-api:user-detail"},
            # 'user': {'view_name': "shelves-api:user-detail"},
        }

'''
# NOTE: HyperlinkedModelSerializer doesn't entirely support namespaces.
# https://stackoverflow.com/questions/27728989/
class BinderSerializer(serializers.HyperlinkedModelSerializer):

    # NOTE: Make readonly fields
    # customer = serializers.StringRelatedField()
    # container = serializers.PrimaryKeyRelatedField(read_only=True)

    # NOTE: Make customer and container writable fields
    customer_id = serializers.PrimaryKeyRelatedField(
        queryset=Customer.objects.all(), source='customer')
    container_id = serializers.PrimaryKeyRelatedField(
        queryset=Container.objects.all(), source='container')

    def validate(self, data):
        """
        Raise error when a customer has already been associated with a binder.

        """

        binders = Binder.objects.all()
        customers_id = list(map(lambda x: x.customer.id, binders))
        if data.get('customer').id in customers_id:
            from django.core.exceptions import ValidationError
            raise ValidationError('This field must be unique.')
        return data

    class Meta:
        model = Binder
        fields = (
            'url', 'id', 'title', 'color', 'content', 'customer_id',
            'container_id')
        extra_kwargs = {
            'url': {'view_name': "shelves-api:binder-detail"},
            # 'customer': {'view_name': "shelves-api:customer-detail"},
            # 'container': {'view_name': "shelves-api:container-detail"},
        }
'''

'''
class BinderCustomerSerializer(serializers.ModelSerializer):
    """For the specific use of the ``BinderSerializer``.

    - Remove ``UniqueValidator`` from the Customer validators;
    - Allow a blank customer code field.

    """

    def validate(self, data):
        """
        Raise validation errors for the customer nested serializer.
        Hence the unique validator has been excluded from the serializer class.

        .. _Optional fields:
           http://www.django-rest-framework.org/api-guide/validators/#optional-fields

        """

        # print('\033[1m' 'DEBUG')

        instances = Customer.objects.all()
        customers = list(map(lambda c: OrderedDict(
            name=c.name,
            code=c.code
        ), instances))
        customers_codes = [c['code'] for c in customers]

        if not data.get('code') and data.get('name'):
            raise ValidationError(
                'Not a valid customer: '
                'The customer code is required within the customer name.')

        if data.get('code'):

            if data not in customers and data.get('code') in customers_codes:
                raise ValidationError(
                    'Not a valid customer: '
                    'The customer code does not mach with the customer name.')

            # NOTE: Get customer
            binders = Binder.objects.all()
            binders_customers = [b.customer for b in binders]
            # Filter out binders without a customer
            binders_customers = list(filter(None, binders_customers))
            binders_customers_codes = [c.code for c in binders_customers]
            if data.get('code') in binders_customers_codes:
                raise ValidationError('This customer has already a binder.')

        # print('\033[0m')

        return data

    class Meta:
        model = Customer
        fields = ('id', 'name', 'code')
        # HACK: Nested serializer with unique constrain.
        # https://github.com/encode/django-rest-framework/issues/2996
        extra_kwargs = {
            'code': {
                # Allow to associate an existent customer to a binder.
                # http://www.django-rest-framework.org/api-guide/validators/#limitations-of-validators
                'validators': [],
                # Allow to create a binder without an associate customer.
                'allow_blank': True
            },
        }


class BinderSerializer(serializers.ModelSerializer):

    # HACK: Writable nested serializer is not automatic.
    # https://github.com/encode/django-rest-framework/issues/2996
    customer = BinderCustomerSerializer(many=False, read_only=False)

    # TODO: Validate the unique code field.
    def create(self, validated_data):
        customer_data = validated_data.pop('customer')

        # NOTE: Logging the binder.
        logger = logging.getLogger()
        logger.info("The context request user.")
        logger.debug(self.context['request'].user)
        logger.debug(self)

        if customer_data.get("code"):
            # Create customer
            customer, created = Customer.objects.get_or_create(
                author=self.context['request'].user,
                **customer_data)
            # Create binder with customer
            binder = Binder.objects.create(customer=customer, **validated_data)
        else:
            # Create binder without customer
            binder = Binder.objects.create(**validated_data)
        return binder

    url = serializers.HyperlinkedIdentityField(
        view_name="shelves-api:binder-detail",
    )

    class Meta:
        model = Binder
        fields = (
            'url',
            'id',
            'title',
            'color',
            'content',
            'container',
            'customer',
            'updated'
        )
'''

class BinderListSerializer(serializers.ModelSerializer):

    url = serializers.HyperlinkedIdentityField(
        view_name="shelves-api:binder-detail",
    )

    customer = CustomerSerializer(many=False, read_only=True)

    class Meta:
        model = Binder
        fields = (
            'url',
            'id',
            'title',
            'color',
            'content',
            'container',
            'customer',
            'updated'
        )


class BinderCreateRetrieveUpdateDestroySerializer(serializers.ModelSerializer):

    class Meta:
        model = Binder
        fields = (
            'id',
            'title',
            'color',
            'content',
            'container',
            'customer',
            'updated'
        )


class ContainerSerializer(serializers.HyperlinkedModelSerializer):

    binder_set = BinderListSerializer(many=True, read_only=True)
    coords = serializers.SerializerMethodField()

    def get_coords(self, obj):
        """Get coordinates as an array."""
        return [obj.col, obj.row]

    class Meta:
        model = Container
        fields = ('url', 'id', 'binder_set', 'coords')
        extra_kwargs = {
            'url': {'view_name': "shelves-api:container-detail"},
        }


class ShelfListSerializer(serializers.HyperlinkedModelSerializer):
    """Writable nested serializers.

    TODO: Write from shelf
    http://www.django-rest-framework.org/api-guide/relations/#writable-nested-serializers
    """

    # container_set = serializers.StringRelatedField(many=True)
    container_set = ContainerSerializer(many=True, read_only=True)

    '''
    # NOTE: Validate author as a CharField (username).
    # author_username = serializers.CharField(source='author')

    def create(self, validated_data):
        """Create a new shelf.

        The ``author_username`` CharField must be converted in
        the ``author`` User Object.
        """

        username = validated_data.get('author')
        author = User.objects.get(username=username)
        validated_data['author'] = author
        return Shelf.objects.create(**validated_data)
    '''

    class Meta:
        model = Shelf
        # NOTE: The author is created from the generic view.
        fields = (
            # 'author_username',
            'url', 'id', 'name', 'cols', 'rows', 'nums', 'container_set'
        )
        extra_kwargs = {
            'url': {'view_name': "shelves-api:shelf-detail"},
            # 'author': {'view_name': "shelves-api:user-detail"},
        }


class ShelfDetailSerializer(serializers.HyperlinkedModelSerializer):

    container_set = ContainerSerializer(many=True, read_only=True)
    # NOTE: Make dimensional fields read only
    cols = serializers.IntegerField(read_only=True)
    rows = serializers.IntegerField(read_only=True)
    nums = serializers.IntegerField(read_only=True)

    class Meta:
        model = Shelf
        fields = ('name', 'desc', 'cols', 'rows', 'nums', 'container_set')
