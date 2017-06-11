# -*- coding: utf-8 -*-
from django.utils.translation import ugettext_lazy as _

# Application Authors
# https://docs.djangoproject.com/en/1.9/ref/applications/#for-application-authors
from django.apps import AppConfig

class StocksConfig(AppConfig):
    name = 'stocks'
    verbose_name = _('Stocks')
