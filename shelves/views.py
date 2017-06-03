from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.core.exceptions import ValidationError
from django.core.files.storage import default_storage
from django.utils.translation import ugettext as _

from .forms import UploadForm
from .models import Customer

import csv
import codecs # Python 2
from io import TextIOWrapper # Python 3


def import_data(request):
    if request.method == 'POST':
        form = UploadForm(request.POST, request.FILES)
        if form.is_valid():
            
            '''NOTE: Moved directly to Upload model so we just need to save the form
            csv_data = request.FILES['csv_file']
            f = TextIOWrapper(request.FILES['csv_file'].file, encoding='utf-8', errors='replace') # Python 3

            # dialect = csv.Sniffer().sniff(codecs.EncodedFile(csv_data, "utf-8").read(1024)) # Python 2
            dialect = csv.Sniffer().sniff(f.read(1024)) # Python 3

            csv_data.open()

            # has_header = csv.Sniffer().has_header(codecs.EncodedFile(csv_data, "utf-8").read(1024)) # Python 2
            has_header = csv.Sniffer().has_header(f.read(1024)) # Python 3

            # csv_data.seek(0) # Python 2
            f.seek(0) # Python 3

            if has_header:

                # reader = csv.DictReader(codecs.EncodedFile(csv_data, "utf-8"), delimiter=',', dialect=dialect) # Python 2
                reader = csv.DictReader(f, delimiter=',', dialect=dialect) # Python 3

                # NOTE: We do not need to skip the header if we use DictReader() instead of reader()
                # next(reader)

                for row in reader:
                    obj, created = Customer.objects.get_or_create(nome=row['nome'], codice=row['codice'])

                # Save the uploaded file in media
                form.save()

            else:
                raise ValidationError(_('The CSV file require an appropriate header '\
                    'in order to spot the corresponding model fields.'), code='invalid')

            csv_data.close()
            '''

            form.save()


    else:
        form = UploadForm()

    entries = Customer.objects.all()

    context = {
        'form': form,
        'entries': entries
    }

    return render(request, 'shelves/index.html', context)
