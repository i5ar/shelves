import os
import logging
# from collections import OrderedDict

from django.contrib.auth.models import User
from django.conf import settings
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from rest_framework import serializers

from ..models import (
    Customer,
    Shelf,
    Binder,
    Upload,
)

# NOTE: Logging configuration used by the debug window in `startsession.sh`.
logging.basicConfig(
    filename=os.path.join(settings.BASE_DIR, 'api.log'),
    level=logging.DEBUG if settings.DEBUG else logging.WARNING,
    format="%(levelname)s %(asctime)s %(message)s",
    filemode="w"  # Run `tail` with `-vn +1` option to output all the rows
)


class UserSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = User
        fields = (
            'url',
            'id',
            'username'
        )
        extra_kwargs = {
            'url': {'view_name': "shelves-api:user-detail"},
        }


class CustomerSerializer(serializers.HyperlinkedModelSerializer):
    def validate(self, data):
        """Validate unique together ``author`` and ``code`` fields."""
        custs = Customer.objects.filter(author=self.context['request'].user)
        # print('{:#^79}'.format(' Get all author instances but current '))
        instances = filter(lambda x: x != self.instance, custs)
        if data.get('code') in map(lambda x: x.code, instances):
            raise ValidationError(_('Customer with this Code already exists.'))
        return data

    class Meta:
        model = Customer
        # NOTE: The author is created from the generic view.
        fields = (
            'url',
            'name',
            'code',
            'note'
        )
        extra_kwargs = {
            'url': {
                'view_name': "shelves-api:customer-detail",
                'lookup_field': "code"
            },
        }


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
            'customer',
            'shelf',
            'col',
            'row',
            'updated'
        )


class BinderCreateRetrieveUpdateDestroySerializer(serializers.ModelSerializer):
    def validate(self, data):
        if data.get('shelf').cols:
            if data.get('col') and not data.get('row'):
                raise ValidationError(_("Row required with col."))
            if not data.get('col') and data.get('row'):
                raise ValidationError(_("Col required with row."))
            if data.get('col') and data.get('col') > data.get('shelf').cols:
                raise ValidationError(_("Value too big."))
            if data.get('row') and data.get('row') > data.get('shelf').rows:
                raise ValidationError(_("Value too big."))
        else:
            if data.get('col') and data.get('row'):
                raise ValidationError(_("Shelf has not a size."))
        return data

    class Meta:
        model = Binder
        fields = (
            'id',
            'title',
            'color',
            'content',
            'customer',
            'shelf',
            'col',
            'row',
            'updated'
        )


class ShelfListSerializer(serializers.HyperlinkedModelSerializer):
    """Writable nested serializers.

    TODO: Write from shelf
    http://www.django-rest-framework.org/api-guide/relations/#writable-nested-serializers
    """
    def validate(self, data):
        """Validate unique together ``author`` and ``code`` fields."""
        shelves = Shelf.objects.filter(author=self.context['request'].user)
        if data.get('code') in map(lambda x: x.code, shelves):
            raise ValidationError(_('Shelf with this Code already exists.'))
        if data.get('cols') and not data.get('rows'):
            raise ValidationError(_("Rows required with cols."))
        if not data.get('cols') and data.get('rows'):
            raise ValidationError(_("Cols required with rows."))
        return data

    class Meta:
        model = Shelf
        # NOTE: The author is created from the generic view.
        fields = (
            # 'author_username',
            'url',
            'id',
            'name',
            'code',
            'cols',
            'rows',
        )
        extra_kwargs = {
            'url': {
                'view_name': "shelves-api:shelf-detail",
                'lookup_field': "code"
            }
        }


class ShelfDetailSerializer(serializers.ModelSerializer):

    # NOTE: Make dimensional fields read only.
    cols = serializers.IntegerField(read_only=True)
    rows = serializers.IntegerField(read_only=True)

    def validate(self, data):
        """Validate unique together ``author`` and ``code`` fields."""
        shelves = Shelf.objects.filter(author=self.context['request'].user)
        instances = filter(lambda x: x != self.instance, shelves)
        if data.get('code') in map(lambda x: x.code, instances):
            raise ValidationError(_('Shelf with this Code already exists.'))
        return data

    class Meta:
        model = Shelf
        fields = (
            'name',
            'code',
            'desc',
            'cols',
            'rows',
        )


class UploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Upload
        fields = (
            'csv_file',
        )
