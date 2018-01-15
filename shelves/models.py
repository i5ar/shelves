# import json
import uuid

from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.utils.translation import ugettext_lazy as _
# from django.contrib.auth.models import User


class Customer(models.Model):
    # TODO: Remove if the router uses the code field instead of the uuid field.
    uuid = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False
    )
    # user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(_('Name'), max_length=32, blank=True)

    # @property
    # def name(self):
    #     """Avoid breaking change.
    #     If the previous model had a `name` field the property decorator will
    #     prevent errors if a `customer.name` is used somewhere else.
    #     """
    #     return self.user.username

    code = models.SlugField(
        _('Code'),
        max_length=16,
        help_text=_(
            "The customer code must not be confused with the customer id "
            "or the user id!"
        )
    )
    note = models.TextField(_('Note'), max_length=128, blank=True)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE
    )

    def __str__(self):
        # return self.user.username
        return '{}'.format(self.uuid)

    class Meta:
        verbose_name = _('Customer')
        verbose_name_plural = _('Customers')
        unique_together = (("code", "author"),)


'''
class BinAmbiguous(models.Model):
    coordinate = models.CharField(
        _('Coordinate'), unique=True, max_length=64,
        help_text='JSON values: Ex. [1, 2]')

    # https://stackoverflow.com/questions/22340258/django-list-field-in-model
    def set_coordinate(self, coord):
        self.coordinate = json.dumps(coord)

    def get_coordinate(self):
        return json.loads(self.coordinate)

    def clean(self):
        """Validate coordinate field."""
        try:
            json.loads(self.coordinate)
        except ValueError as e:
            try:
                list_str = self.coordinate.split(',')  # ['1', '2']
                list_int = list(map(int, list_str))  # [1, 2]
                self.coordinate = json.dumps(list_int)
            except:
                raise ValidationError(e)

    def __str__(self):
        return '{}'.format(self.coordinate)
'''


class Shelf(models.Model):
    """Regular or irregular furniture."""
    name = models.CharField(
        _('Name'), max_length=64,
        help_text=_('A name for the shelf.'))
    code = models.SlugField(max_length=16,)
    desc = models.TextField(_('Description'), blank=True)
    cols = models.PositiveIntegerField(
        _('Columns'), validators=[MinValueValidator(1)],
        help_text=_('The number of cols'), blank=True, null=True)
    rows = models.PositiveIntegerField(
        _('Rows'), validators=[MinValueValidator(1)],
        help_text=_('The number of rows'), blank=True, null=True)
    nums = models.PositiveIntegerField(
        _('Containers number'), validators=[MinValueValidator(1)],
        help_text=_('The number of containers'), blank=True, null=True)

    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def clean(self):
        """Validate columns and rows fields.

        The cleaning method doesn't run when the fields are passed through the
        REST API.
        """
        if not self.cols and self.rows:
            raise ValidationError(
                _("The columns field is required within the rows field."))
        elif self.cols and not self.rows:
            raise ValidationError(
                _("The rows field is required within the columns field."))
        elif not self.cols and not self.rows and not self.nums:
            raise ValidationError(
                _("At least one dimensional value is required."))

        if self.cols and self.rows and self.cols*self.rows > 2**6:
            raise ValidationError(_("Too much containers for one shelf."))
        elif self.nums and self.nums > 2**6:
            raise ValidationError(_("Too much containers."))

    def save(self, *args, **kwargs):
        """Update or create containers."""
        if self.id:
            # NOTE: Update containers.
            super(Shelf, self).save(*args, **kwargs)
        else:
            # NOTE: Create containers.
            if self.cols and self.rows:
                self.nums = self.cols*self.rows
                super(Shelf, self).save(*args, **kwargs)
                for col in range(self.cols):
                    for row in range(self.rows):
                        container = Container(
                            shelf=self, col=col+1, row=row+1)
                        container.save()
            elif self.nums:
                super(Shelf, self).save(*args, **kwargs)
                for __ in range(self.nums):
                    container = Container(shelf=self)
                    container.save()

    def __str__(self):
        return '{}'.format(self.id)

    class Meta:
        verbose_name = _('Shelf')
        verbose_name_plural = _('Shelves')
        unique_together = (("code", "author"),)


class ContainerManager(models.Manager):
    """HACK: Reverse the order for the chart."""
    def get_queryset(self):
        return super().get_queryset().order_by('-id')


class Container(models.Model):
    """Shelf units."""

    shelf = models.ForeignKey(Shelf, on_delete=models.CASCADE)
    col = models.IntegerField(_('Column'), blank=True, null=True)
    row = models.IntegerField(_('Row'), blank=True, null=True)
    # jsoncoord = models.CharField(_('Coordinate'), max_length=64, blank=True)

    # objects = ContainerManager()

    def __str__(self):
        return '{}'.format(self.id)

    # def save(self, *args, **kwargs):
    #     """Add a jsoncoord field based on the row and the column."""
    #     list_int = [self.col, self.row]
    #     self.jsoncoord = json.dumps(list_int)
    #     super(Container, self).save(*args, **kwargs)

    class Meta:
        verbose_name = _('Container')
        verbose_name_plural = _('Containers')


class Binder(models.Model):
    """The binder is unique for each customer."""
    title = models.CharField(max_length=64, blank=False)
    customer = models.OneToOneField(
        'Customer', on_delete=models.CASCADE,  # related_name='customer'
        blank=True, null=True)
    container = models.ForeignKey(
        Container, on_delete=models.CASCADE)
    content = models.TextField(_('Binder content'), blank=True)
    color = models.CharField(
        _('Color'), blank=True, max_length=6, help_text=_('Hex value.'))
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '{}'.format(self.id)

    class Meta:
        verbose_name = _('Binder')
        verbose_name_plural = _('Binders')


class Upload(models.Model):
    """Upload Customers"""
    csv_file = models.FileField('File CSV', upload_to='docs')
    created = models.DateField(auto_now_add=True)
