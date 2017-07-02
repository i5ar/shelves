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
    code = models.IntegerField(_('Code'), null=True, unique=True,
        help_text=_('Customer code must not be confused with user code!'))

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
    coordinate = models.CharField(_('Coordinate'), unique=True, max_length=64,
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
                list_str = self.coordinate.split(',') # ['1', '2']
                list_int = list(map(int, list_str)) # [1, 2]
                self.coordinate = json.dumps(list_int)
            except:
                raise ValidationError(e)

    def __str__(self):
        return '{}'.format(self.coordinate)


class RegularShelf(models.Model):
    name = models.CharField(_('Shelf name'), max_length=64, blank=True,
        null=True)
    cols = models.IntegerField(_('Columns'), help_text=_('Number of cols'))
    rows = models.IntegerField(_('Rows'), help_text=_('Number of rows'))

    def save(self, *args, **kwargs):
        super(RegularShelf, self).save(*args, **kwargs)
        for col in range(self.cols):
            for row in range(self.rows):
                RegularBin(col=col+1, row=row+1, shelf=self).validate_unique()
                RegularBin(col=col+1, row=row+1, shelf=self).save()

    def __str__(self):
        return str(self.name)

    class Meta:
        verbose_name = _('Shelf')
        verbose_name_plural = _('Shelves')


class RegularBin(models.Model):
    col = models.IntegerField(_('Column'))
    row = models.IntegerField(_('Row'))
    coordinate = models.CharField(_('Coordinate'), max_length=64, blank=True)
    shelf = models.ForeignKey('RegularShelf', on_delete=models.CASCADE)

    def validate_unique(self, exclude=None):
        if RegularBin.objects.filter(
                col=self.col, row=self.row, shelf=self.shelf).exists():
            raise ValidationError(_('Coordinate must be unique'))

    def save(self, *args, **kwargs):
        list_int = [self.col, self.row]
        self.coordinate = json.dumps(list_int)
        super(RegularBin, self).save(*args, **kwargs)

    def __str__(self):
        return '{} {}'.format(self.shelf, self.coordinate)

    class Meta:
        verbose_name = _('Bin')
        verbose_name_plural = _('Bins')


class Binder(models.Model):
    biography = models.OneToOneField('Customer', on_delete=models.CASCADE,
        related_name='biography')
    regular_bin = models.ForeignKey('RegularBin', on_delete=models.CASCADE,
        null=True)

    def __str__(self):
        return str(self.biography)

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
                        Integrity error may happen if 2 customers have same code
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
                            cust, created_cust = Customer.objects.get_or_create(
                                user=row[_('username')], code=row[_('code')])
                        except:
                            raise ValidationError('Is the field {} present in '\
                                'the CSV header?'.format(e), code='key')

            else:
                raise ValidationError(_('The CSV file require a proper header '\
                    'in order to spot the corresponding model fields.'),
                    code='invalid')
