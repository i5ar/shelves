# import json

from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.utils.translation import ugettext_lazy as _
# from django.contrib.auth.models import User


class Customer(models.Model):
    name = models.CharField(_('Name'), max_length=32, blank=True)
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
        return '{}'.format(self.code)

    class Meta:
        verbose_name = _('Customer')
        verbose_name_plural = _('Customers')
        unique_together = (("code", "author"),)


class Shelf(models.Model):
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

    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def clean(self):
        """Validate columns and rows fields."""
        if self.cols and not self.rows:
            raise ValidationError(_("Rows required with cols."))
        if not self.cols and self.rows:
            raise ValidationError(_("Cols required with rows."))

    def __str__(self):
        return '{}'.format(self.code)

    class Meta:
        verbose_name = _('Shelf')
        verbose_name_plural = _('Shelves')
        unique_together = (("code", "author"),)


class Binder(models.Model):
    title = models.CharField(max_length=64, blank=False)
    customer = models.OneToOneField(
        'Customer', on_delete=models.CASCADE,  # related_name='customer'
        blank=True, null=True)
    shelf = models.ForeignKey(
        Shelf, on_delete=models.CASCADE)
    col = models.IntegerField(null=True, blank=True)
    row = models.IntegerField(null=True, blank=True)
    content = models.TextField(_('Binder content'), blank=True)
    color = models.CharField(
        _('Color'), blank=True, max_length=6, help_text=_('Hex value.'))
    updated = models.DateTimeField(auto_now=True)

    def clean(self):
        if self.shelf.cols:
            if self.col and not self.row:
                raise ValidationError(_("Row required with col."))
            if not self.col and self.row:
                raise ValidationError(_("Col required with row."))
            if self.col and self.col > self.shelf.cols:
                raise ValidationError(_("Value too big."))
            if self.row and self.row > self.shelf.rows:
                raise ValidationError(_("Value too big."))
        else:
            if self.col or self.row:
                raise ValidationError(_("Shelf has not a size."))

    def __str__(self):
        return '{}'.format(self.id)

    class Meta:
        verbose_name = _('Binder')
        verbose_name_plural = _('Binders')


class Attached(models.Model):
    """Binder attachments."""
    title = models.CharField(_('Title'), max_length=64)
    binder = models.ForeignKey('Binder', on_delete=models.CASCADE)
    file = models.FileField(upload_to='docs')

    class Meta:
        verbose_name = _('Attachment')
        verbose_name_plural = _('Attachments')

    def __str__(self):
        return self.title


class Upload(models.Model):
    """Upload customers."""
    csv_file = models.FileField('File CSV', upload_to='docs')
    created = models.DateField(auto_now_add=True)
