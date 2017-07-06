from django.contrib.auth.models import User

from rest_framework import serializers

from ..models import (
    Customer,
    Bin,
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

    '''
    customer = serializers.CharField()

    def create(self, validated_data):
        """Create a new customer.

        The `user` field as defined above is a username, so it must be
        converted in a User object
        """
        username = validated_data.get('customer')
        user = User.objects.get(username=username)
        customer = Customer.objects.get(user=user)
        validated_data['customer'] = customer
        return Binder.objects.create(**validated_data)
    '''

    class Meta:
        model = Binder
        fields = ('url', 'customer', 'bin', 'color', 'name', 'content')
        extra_kwargs = {
            'url': {'view_name': "shelves-api:binder-detail"},
            'customer': {'view_name': "shelves-api:customer-detail"},
            'bin': {'view_name': "shelves-api:bin-detail"},
        }


class BinSerializer(serializers.HyperlinkedModelSerializer):

    binder_set = BinderSerializer(many=True, read_only=True)

    col_row = serializers.SerializerMethodField('set_col_row')

    def set_col_row(self, obj):
        """Define a custom field instead of coordinate field."""
        return [obj.col, obj.row]

    class Meta:
        model = Bin
        fields = ('url', 'col_row', 'binder_set')
        extra_kwargs = {
            'url': {'view_name': "shelves-api:bin-detail"},
        }


class ShelfSerializer(serializers.HyperlinkedModelSerializer):
    """Writable nested serializers.

    TODO: Write from shelf
    http://www.django-rest-framework.org/api-guide/relations/#writable-nested-serializers
    """

    # bin_set = serializers.StringRelatedField(many=True)
    bin_set = BinSerializer(many=True, read_only=True)

    class Meta:
        model = Shelf
        fields = ('url', 'name', 'cols', 'rows', 'bin_set')
        extra_kwargs = {
            'url': {'view_name': "shelves-api:shelf-detail"},
        }
