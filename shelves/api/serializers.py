from django.contrib.auth.models import User

from rest_framework import serializers

from ..models import (
    Customer,
    RegularBin,
    RegularShelf,
    Binder,
)


# class CustomerSerializer(serializers.ModelSerializer):
#     """Used with CustomerListAPIView."""
#     class Meta:
#         model = Customer
#         fields = ('code', 'user')


class CustomerHyperlinkedSerializer(serializers.HyperlinkedModelSerializer):
    """Customer Serializers."""

    # Since `user` is `OneToOneField` we must specify where does it come from
    user = serializers.CharField(source='user.username')

    class Meta:
        model = Customer
        fields = ('user', 'code', 'url')
        # http://www.django-rest-framework.org/api-guide/serializers/
        extra_kwargs = {
            'url': {'view_name': "shelves-api:customer-detail"},
        }

    def create(self, validated_data):
        """Create a new customer.

        The `user` field as defined above is a username, so it must be
        converted in a User object
        """
        _username = validated_data.get('user').get('username')
        _user = User.objects.get(username=_username)
        validated_data['user'] = _user
        return Customer.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """Update a new customer.

        The `user` field as defined above is a username, so it must be
        converted in a User object
        """
        _username = validated_data.get('user').get('username')
        instance.user = User.objects.get(username=_username)
        instance.code = validated_data.get('code', instance.code)
        instance.save()
        return instance


class RegularBinHyperlinkedSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = RegularBin
        fields = ('coordinate', 'url', 'shelf')
        # http://www.django-rest-framework.org/api-guide/serializers/
        extra_kwargs = {
            'url': {'view_name': "shelves-api:regularbin-detail"},
            'shelf': {'view_name': "shelves-api:regularshelf-detail"},
        }


class RegularShelfHyperlinkedSerializer(
        serializers.HyperlinkedModelSerializer):
    class Meta:
        model = RegularShelf
        fields = ('name', 'cols', 'rows', 'url')
        extra_kwargs = {
            'url': {'view_name': "shelves-api:regularshelf-detail"},
        }


class BinderHyperlinkedSerializer(serializers.HyperlinkedModelSerializer):
    biography = serializers.CharField()

    class Meta:
        model = Binder
        fields = ('biography', 'url', 'regular_bin')
        extra_kwargs = {
            'url': {'view_name': "shelves-api:binder-detail"},
            'regular_bin': {'view_name': "shelves-api:regularbin-detail"},
        }


###############################################################################


class RegularShelfSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = RegularShelf
        fields = ('url', 'name', 'cols', 'rows')
        extra_kwargs = {
            'url': {'view_name': "shelves-api:regularshelf-detail"},
        }


class CustomerSerializer(serializers.HyperlinkedModelSerializer):
    # user = serializers.CharField(source='user.id')

    class Meta:
        model = Customer
        fields = ('url', 'user', 'code')
        extra_kwargs = {
            'url': {'view_name': "shelves-api:customer-detail"},
            'user': {'view_name': "shelves-api:user-detail"},
        }


class UserSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = User
        fields = ('url', 'id', 'username')
        extra_kwargs = {
            'url': {'view_name': "shelves-api:user-detail"},
        }
