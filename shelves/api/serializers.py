from django.contrib.auth.models import User

from rest_framework import serializers

from ..models import Customer


class CustomerHyperlinkedSerializer(serializers.HyperlinkedModelSerializer):
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
        The `user` field as defined above is a username, so it must be converted
        in a User object
        """
        _username=validated_data.get('user').get('username')
        _user, created = User.objects.get_or_create(username=_username)
        validated_data['user'] = _user
        return Customer.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """Update a new customer.
        The `user` field as defined above is a username, so it must be converted
        in a User object
        """
        _username=validated_data.get('user').get('username')
        instance.user = User.objects.get(username=_username)
        instance.code = validated_data.get('code', instance.code)
        instance.save()
        return instance

# class CustomerSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Customer
#         fields = ('code', 'user')
