from django.db import models
from django.core.exceptions import ValidationError
from django.core.files.storage import default_storage
from django.utils.translation import ugettext_lazy as _

import json
import csv


class Customer(models.Model):
    codice = models.IntegerField()
    nome = models.CharField(max_length=64, blank=True, null=True)

    def __str__(self):
        return str(self.nome)


class BinAmbiguous(models.Model):
    coordinate = models.CharField(unique=True, max_length=64, help_text="JSON values: Ex. [1, 2]")

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
        return "{}".format(self.coordinate)


BIN_HELP_TEXT = _("Please, use 0 if you can\'t assign coordinates.")
class Bin(models.Model):
    row = models.IntegerField(help_text=BIN_HELP_TEXT)
    col = models.IntegerField(help_text=BIN_HELP_TEXT)
    coordinate = models.CharField(max_length=64, blank=True)

    def validate_unique(self, exclude=None):
        if self.row != 0 and self.col != 0:
            if Bin.objects.filter(row=self.row, col=self.col).exists():
                raise ValidationError('Coordinate must be unique')

    def save(self, *args, **kwargs):
        list_int = [self.row, self.col]
        self.coordinate = json.dumps(list_int)
        super(Bin, self).save(*args, **kwargs)

    def __str__(self):
        return "{}".format(self.coordinate)


class Shelf(models.Model):
    name = models.CharField(max_length=64, blank=True, null=True)
        
    def __str__(self):
        return str(self.name)


class Binder(models.Model):
    biography = models.OneToOneField('Customer', on_delete=models.CASCADE, related_name="biography")
    shelf = models.ForeignKey('Shelf', on_delete=models.CASCADE)
    shelf_bin = models.ForeignKey('Bin', on_delete=models.CASCADE)

    def __str__(self):
        return str(self.biography)


class Upload(models.Model):
    csv_file = models.FileField(upload_to='docs')

    def save(self, *args, **kwargs):
        super(Upload, self).save(*args, **kwargs)

        # http://stackoverflow.com/questions/2459979/how-to-import-csv-data-into-django-models
        with open(default_storage.path(self.csv_file)) as f:
            has_header = csv.Sniffer().has_header(f.read(1024))
            f.seek(0)
            if has_header:
                reader = csv.DictReader(f)
                for row in reader:
                    obj, created = Customer.objects.get_or_create(nome=row['nome'], codice=row['codice'])
            else:
                raise ValidationError(_('The CSV file require an appropriate header '\
                    'in order to spot the corresponding model fields.'), code='invalid')
