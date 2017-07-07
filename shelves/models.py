from django.db import models
from django.core.exceptions import ValidationError
from django.core.files.storage import default_storage
from django.utils.translation import ugettext_lazy as _
from django.db import IntegrityError
from django.contrib.auth.models import User

import json
import csv


class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    code = models.IntegerField(
        _('Code'), null=True, unique=True,
        help_text=_('Customer code must not be confused with user code!')
    )

    @property
    def name(self):
        """Avoid breaking change.
        The previus model had a `name` field so the property decorator will
        prevent errors if a `customer.name` is used somewhere else.
        """
        return self.user.username

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = _('Customer')
        verbose_name_plural = _('Customers')


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
        '''Validate coordinate field'''
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


class Shelf(models.Model):
    """Regular or irregular forniture."""
    name = models.CharField(
        _('Name'), max_length=64,
        help_text=_('A name for the shelf.'), unique=True)
    desc = models.TextField(_('Description'),  blank=True)
    cols = models.IntegerField(
        _('Columns'), help_text=_('The number of cols'), blank=True, null=True)
    rows = models.IntegerField(
        _('Rows'), help_text=_('The number of rows'), blank=True, null=True)
    nums = models.PositiveIntegerField(
        _('Containers'), help_text=_('The number of containers'),
        blank=True, null=True)

    def clean(self):
        """Validate columns and rows fields.

        Make sure both fields are inserted.
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

    def save(self, *args, **kwargs):
        """Create container and boards.

        Create both containers and boards when the shelf columns and rows are
        provided. When the shelf is irregular no board will be created.
        """
        if self.id:  # Update
            if self.cols and self.rows:
                self.name = self.name
                self.desc = self.desc
                self.nums = self.cols*self.rows
                super(Shelf, self).save(*args, **kwargs)
            elif self.nums:
                self.name = self.name
                self.desc = self.desc
                super(Shelf, self).save(*args, **kwargs)
        else:  # Create
            if self.cols and self.rows:
                # Create containers and store them in a list for later and save
                self.name = self.name
                self.desc = self.desc
                self.nums = self.cols*self.rows
                super(Shelf, self).save(*args, **kwargs)
                for col in range(self.cols):
                    for row in range(self.rows):
                        container = Container(shelf=self)
                        container.save()
                        board = Board(
                            col=col+1, row=row+1, container=container)
                        board.save()
            elif self.nums:
                self.name = self.name
                self.desc = self.desc
                super(Shelf, self).save(*args, **kwargs)
                for num in range(self.nums):
                    container = Container(shelf=self)
                    container.validate_unique()
                    container.save()

    def __str__(self):
        return '{}'.format(self.name)

    class Meta:
        verbose_name = _('Shelf')
        verbose_name_plural = _('Shelves')


class Container(models.Model):
    """Shelf units."""

    shelf = models.ForeignKey(Shelf, on_delete=models.CASCADE)

    def __str__(self):
        return '{}'.format(self.id)

    class Meta:
        verbose_name = _('Container')
        verbose_name_plural = _('Containers')


class Board(models.Model):
    """Regular shelf boards."""

    col = models.IntegerField(_('Column'))
    row = models.IntegerField(_('Row'))
    # jsoncoord = models.CharField(_('Coordinate'), max_length=64, blank=True)
    container = models.OneToOneField(Container, on_delete=models.CASCADE)

    # def save(self, *args, **kwargs):
    #     """Add a jsoncoord field based on the row and the column."""
    #     list_int = [self.col, self.row]
    #     self.jsoncoord = json.dumps(list_int)
    #     super(Board, self).save(*args, **kwargs)

    def __str__(self):
        return '{}'.format(self.container)

    class Meta:
        verbose_name = _('Board')
        verbose_name_plural = _('Boards')


class Binder(models.Model):
    """The binder is unique for each customer"""
    customer = models.OneToOneField(
        'Customer', on_delete=models.CASCADE,  # related_name='customer'
        blank=True, null=True)
    container = models.ForeignKey(
        Container, on_delete=models.CASCADE, null=True)
    content = models.TextField(_('Binder content'), blank=True)
    color = models.CharField(
        _('Color'), blank=True, max_length=6, help_text=_('Hex value.'))
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '{}'.format(self.customer)

    class Meta:
        verbose_name = _('Binder')
        verbose_name_plural = _('Binders')


class Upload(models.Model):
    csv_file = models.FileField('File CSV', upload_to='docs')

    def save(self, *args, **kwargs):
        super(Upload, self).save(*args, **kwargs)

        # http://stackoverflow.com/questions/2459979/how-to-import-csv-data-into-django-models
        with open(default_storage.path(self.csv_file)) as f:
            has_header = csv.Sniffer().has_header(f.read(1024))
            f.seek(0)
            if has_header:
                reader = csv.DictReader(f)
                for row in reader:
                    try:
                        # TODO: Create user only if not exceptions occur
                        user, created_user = User.objects.get_or_create(
                            username=row['username'])
                        cust, created_cust = Customer.objects.get_or_create(
                            user=user, code=row['code'])
                    except IntegrityError as e:
                        '''
                        An integrity error may happen if two customers have the
                        same code.
                        '''
                        print('{0!r}'.format(e))
                        raise ValidationError(e, code='integrity')
                    except KeyError as e:
                        '''
                        Key error may happen if CSV header is divergent
                        from model fields
                        '''
                        try:
                            '''
                            Pretend internationalized field username match the
                            CSV header
                            '''
                            cust, created = Customer.objects.get_or_create(
                                user=row[_('username')], code=row[_('code')])
                        except:
                            raise ValidationError(
                                'Is the field {} present in the CSV file '
                                'header?'.format(e),
                                code='key')

            else:
                raise ValidationError(
                    _('The CSV file require a proper header in order to spot '
                        'the corresponding model fields.'),
                    code='invalid')
