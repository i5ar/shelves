from django.contrib.auth.models import User
from django.conf import settings

from rest_framework import serializers

import os
import logging

from ..models import (
    Customer,
    Container,
    Shelf,
    Binder,
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
            'url', 'id', 'name', 'code')  # `name` previusly `user`
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


class BinderSerializer(serializers.ModelSerializer):
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
            'customer',
            'container',
            'updated'
        )


class ContainerSerializer(serializers.HyperlinkedModelSerializer):

    binder_set = BinderSerializer(many=True, read_only=True)
    coords = serializers.SerializerMethodField()

    def get_coords(self, obj):
        """Set coordinates array instead of separate col and row fields."""
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
            'url', 'id', 'name', 'cols', 'rows', 'nums', 'container_set')
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

    # NOTE: Logging the container set.
    logging.basicConfig(
        filename = os.path.join(settings.BASE_DIR, 'api.log'),
        level = logging.DEBUG if settings.DEBUG else logging.WARNING,
        format = "%(levelname)s %(asctime)s %(message)s",
        filemode = "w"
    )
    logger = logging.getLogger()
    logger.info("Container set.")
    logger.debug(container_set)
