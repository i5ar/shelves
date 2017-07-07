from django.contrib.auth.models import User

from rest_framework import serializers

from ..models import (
    Customer,
    Board,
    Container,
    Shelf,
    Binder,
)


from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from django.utils.six import BytesIO
import json


class UserSerializer(serializers.HyperlinkedModelSerializer):

    customer = serializers.HyperlinkedRelatedField(
        view_name='shelves-api:customer-detail', read_only=True)

    class Meta:
        model = User
        fields = ('url', 'id', 'username', 'customer')
        extra_kwargs = {
            'url': {'view_name': "shelves-api:user-detail"},
        }


class CustomerSerializer(serializers.HyperlinkedModelSerializer):

    '''
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
        fields = ('url', 'user', 'code')
        extra_kwargs = {
            'url': {'view_name': "shelves-api:customer-detail"},
            'user': {'view_name': "shelves-api:user-detail"},
        }


class BinderSerializer(serializers.HyperlinkedModelSerializer):

    # NOTE: Make readonly fields
    # customer = serializers.StringRelatedField()
    # container = serializers.PrimaryKeyRelatedField(read_only=True)

    # NOTE: Make customer and container writable fields
    customer = serializers.CharField()
    container_id = serializers.PrimaryKeyRelatedField(
        queryset=Container.objects.all(), source='container')

    def create(self, validated_data):
        """Create a new binder."""
        # NOTE: Get the user object from the user username
        user_username = validated_data.get('customer')
        user = User.objects.get(username=user_username)
        customer = Customer.objects.get(user=user)
        validated_data['customer'] = customer

        # NOTE: Get the container object from the container id
        # https://groups.google.com/forum/#!topic/django-rest-framework/5twgbh427uQ
        instance = validated_data.get('container')
        container = Container.objects.get(id=instance.id)
        validated_data['container_id'] = container.id

        return Binder.objects.create(**validated_data)

    class Meta:
        model = Binder
        fields = ('url', 'customer', 'color', 'content', 'container_id')
        extra_kwargs = {
            'url': {'view_name': "shelves-api:binder-detail"},
            # 'customer': {'view_name': "shelves-api:customer-detail"},
            # 'container': {'view_name': "shelves-api:container-detail"},
        }


class BoardSerializer(serializers.HyperlinkedModelSerializer):

    col_row = serializers.SerializerMethodField('set_col_row')

    def set_col_row(self, obj):
        """Define a custom field instead of coordinate field."""
        return [obj.col, obj.row]

    class Meta:
        model = Board
        fields = ('url', 'col_row')
        extra_kwargs = {
            'url': {'view_name': "shelves-api:board-detail"},
        }


class ContainerSerializer(serializers.HyperlinkedModelSerializer):

    binder_set = BinderSerializer(many=True, read_only=True)
    board = BoardSerializer(read_only=True)

    class Meta:
        model = Container
        fields = ('url', 'binder_set', 'board')
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

    class Meta:
        model = Shelf
        fields = ('url', 'name', 'cols', 'rows', 'nums', 'container_set')
        extra_kwargs = {
            'url': {'view_name': "shelves-api:shelf-detail"},
        }


class ShelfDetailSerializer(serializers.HyperlinkedModelSerializer):

    container_set = ContainerSerializer(many=True, read_only=True)
    # Make dimensional fields read only
    cols = serializers.IntegerField(read_only=True)
    rows = serializers.IntegerField(read_only=True)
    nums = serializers.IntegerField(read_only=True)

    class Meta:
        model = Shelf
        fields = ('name', 'desc', 'cols', 'rows', 'nums', 'container_set')
