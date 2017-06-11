from __future__ import unicode_literals
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _
from django.db import models
# from django.contrib.sites.models import Site

import math


@python_2_unicode_compatible
class CompanyModel(models.Model):
    # site = models.OneToOneField(Site, on_delete=models.CASCADE)
    name = models.CharField(max_length=64)
    address = models.CharField(max_length=254, blank=True)

    class Meta:
        verbose_name = _('Company')
        verbose_name_plural = _('Companies')

    def __str__(self):              # __unicode__ on Python 2
        return self.name


@python_2_unicode_compatible
class ContractModel(models.Model):
    title = models.CharField(max_length=128)
    content = models.TextField()
    company = models.ForeignKey(CompanyModel, on_delete=models.CASCADE, verbose_name=_('Company'))

    class Meta:
        verbose_name = _('Contract')
        verbose_name_plural = _('Contracts')

    def __str__(self):              # __unicode__ on Python 2
        return self.title


@python_2_unicode_compatible
class LayoutModel(models.Model):
    '''Local Administrative Unit '''
    recipient = models.CharField(_('Recipient'), max_length=128)
    operation = models.CharField(_('Operation'), max_length=256)
    contract = models.ForeignKey(ContractModel, on_delete=models.CASCADE, default=1)
    tep = models.IntegerField(_('tonne of oil equivalent'))
    co2 = models.FloatField(_('tonne/year less emissions of CO2'), blank=True)
    trees = models.IntegerField(_('saved trees'), blank=True)

    # https://docs.djangoproject.com/en/1.9/topics/db/models/#overriding-model-methods
    def save(self, *args, **kwargs):
        if self.tep:
            self.co2 = self.tep*2.35
            self.trees = math.ceil((((self.tep*2.35)*1000)/70)*5)
        super(LayoutModel, self).save(*args, **kwargs)

    class Meta:
        verbose_name = _('Layout')
        verbose_name_plural = _('Layouts')

    def __str__(self):              # __unicode__ on Python 2
        return self.recipient


@python_2_unicode_compatible
class DownloadModel(models.Model):
    recipient = models.ForeignKey(LayoutModel, on_delete=models.CASCADE, verbose_name=_('Local Administrative Unit'))
    name = models.CharField(max_length=64, blank=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created']
        verbose_name = _('Download')
        verbose_name_plural = _('Downloads')

    def __str__(self):              # __unicode__ on Python 2
        return self.name
