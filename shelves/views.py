import operator
from functools import reduce

from django.shortcuts import render
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext as _
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.db.models import Q

from .forms import UploadForm
from .models import Customer, Shelf, Binder

'''
import csv
import codecs  # Python 2
from io import TextIOWrapper  # Python 3
'''


def import_data(request):
    if request.method == 'POST':
        form = UploadForm(request.POST, request.FILES)
        if form.is_valid():

            '''
            Moved directly to Upload model so we just need to save the form

            csv_data = request.FILES['csv_file']
            f = TextIOWrapper(request.FILES['csv_file'].file, encoding='utf-8',
                errors='replace') # Python 3

            # dialect = csv.Sniffer().sniff(
                codecs.EncodedFile(csv_data, "utf-8").read(1024)) # Python 2
            dialect = csv.Sniffer().sniff(f.read(1024)) # Python 3

            csv_data.open()

            # has_header = csv.Sniffer().has_header(codecs.EncodedFile(
                csv_data, "utf-8").read(1024)) # Python 2
            has_header = csv.Sniffer().has_header(f.read(1024)) # Python 3

            # csv_data.seek(0) # Python 2
            f.seek(0) # Python 3

            if has_header:

                # reader = csv.DictReader(
                    codecs.EncodedFile(csv_data, "utf-8"),
                    delimiter=',',
                    dialect=dialect) # Python 2

                reader = csv.DictReader(
                    f,
                    delimiter=',',
                    dialect=dialect) # Python 3

                # NOTE: We don't need to skip the header if we use DictReader()
                # next(reader)

                for row in reader:
                    # Used in the previous Customer model
                    obj, created = Customer.objects.get_or_create(
                        name=row['name'], code=row['code'])

                # Save the uploaded file in media
                form.save()

            else:
                raise ValidationError(_('The CSV file require a proper '\
                    'header in order to spot the corresponding model fields.'),
                    code='invalid')

            csv_data.close()
            '''

            form.save()

    else:
        form = UploadForm()

    customers = Customer.objects.all()
    shelves = Shelf.objects.all()
    binders = Binder.objects.all()

    context = {
        'form': form,
        'customers': customers,
        'shelves': shelves,
        'binders': binders,
    }

    return render(request, 'shelves/index.html', context)


# Search
# https://www.calazan.com/adding-basic-search-to-your-django-site/
class BinderListView(ListView):
    model = Binder
    # paginate_by = 8

    def get_queryset(self):
        """Override queryset.

        Search by
        ``title``,
        ``content``,
        ``customer__code``,
        ``customer__name``.

        """

        queryset = super(BinderListView, self).get_queryset()
        query = self.request.GET.get('q')
        if query:
            query_list = query.split()
            # TODO: DRY because of ``BinderList`` queryset in API.
            queryset = queryset.filter(
                reduce(
                    operator.and_,
                    (Q(title__icontains=q) for q in query_list)
                ) | reduce(
                    operator.and_,
                    (Q(content__icontains=q) for q in query_list)
                ) | reduce(
                    operator.and_,
                    (Q(customer__code__icontains=q) for q in query_list)
                ) | reduce(
                    operator.and_,
                    (Q(customer__name__icontains=q) for q in query_list)
                )
            )

        return queryset


class BinderDetailView(DetailView):
    model = Binder
