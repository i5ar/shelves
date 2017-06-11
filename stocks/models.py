from __future__ import unicode_literals
from django.utils.encoding import python_2_unicode_compatible
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


# https://docs.djangoproject.com/en/1.9/ref/validators/#writing-validators
def valid_pct(value):
    if value > 1 and value <= 100:
        return float(value)/100
    elif value >=0 and value <=1:
        return float(value)
    else:
        raise ValidationError(_('%(value)s is not a valid pct'), params={'value': value},)


@python_2_unicode_compatible
class Dispatched(models.Model):
    '''Dispatched Certification'''
    code = models.CharField(max_length=24)
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    dispatch = models.DateField()
    # approval = models.DateField()

    EI = 8
    FI = 5
    YEARS = (
        (EI, 'Anni 8'),
        (FI, 'Anni 5'),
    )
    years = models.PositiveIntegerField(_('Years'), help_text='<a href="http://www.gse.it" target="_blank"><span class="glyphicon glyphicon-info-sign"></span></a> Anni 5 per impianti; Anni 8 per involucro.', choices=YEARS, null=True, blank=True)
    stock_year = models.PositiveIntegerField(null=True, blank=True)
    customer_pct = models.FloatField(validators=[valid_pct], null=True, blank=True)
    duty = models.CharField(max_length=24, blank=True)
    protocol = models.PositiveIntegerField(null=True, blank=True)

    stock_year_customer = models.FloatField(null=True, blank=True)

    # http://stackoverflow.com/questions/4380879/django-model-field-default-based-off-another-field-in-same-model
    # name = models.CharField("Name", max_length=30)
    # def subject_initials(self):
    #     return ''.join(map(lambda x: '' if len(x)==0 else x[0], self.name.split(' ')))
    # subject_init = models.CharField("Subject Initials", max_length=5, default=self.subject_initials)

    # https://docs.djangoproject.com/en/1.9/topics/db/models/#overriding-model-methods
    def save(self, *args, **kwargs):
        if self.stock_year and self.customer_pct:
            self.stock_year_customer = self.stock_year * self.customer_pct
        super(Dispatched, self).save(*args, **kwargs)

    def __str__(self):              # __unicode__ on Python 2
        return self.code

    class Meta:
        verbose_name = _("Dispatched certification")
        verbose_name_plural = _("Dispatched certifications")


@python_2_unicode_compatible
class Approved(models.Model):
    '''Approved Certification'''
    dispatched = models.ForeignKey(
        'Dispatched',
        on_delete=models.CASCADE,
    )
    approval = models.DateField()

    def __str__(self):              # __unicode__ on Python 2
        return self.dispatched.code
        
    class Meta:
        verbose_name = _("Approved certification")
        verbose_name_plural = _("Approved certifications")
