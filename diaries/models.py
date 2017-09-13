from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.core.validators import EmailValidator
from django.core.exceptions import ValidationError


class Contact(models.Model):
    title = models.CharField(_('Title'), max_length=255, blank=True)
    ADDRESS_CHOICES = (
        ('PH', _('Phone')),
        ('EM', _('Email')),
    )
    address_choice = models.CharField(
        _('Address choice'),
        max_length=2,
        choices=ADDRESS_CHOICES,
        default='PH',
    )
    address = models.CharField(_('Address'), max_length=32)

    registration = models.ForeignKey(
        'RegistrationEvent', on_delete=models.CASCADE)

    def clean(self):
        """Validate the address field if it is an email choice.

        The email validator uses the __call__ method from ``EmailValidator``.
        https://docs.djangoproject.com/en/dev/_modules/django/core/validators/#EmailValidator
        """
        if self.address_choice == 'EM':
            try:
                email_validator = EmailValidator()
                email_validator(self.address)
            except ValidationError as e:
                raise ValidationError(e)

    class Meta:
        verbose_name = _('Contact')
        verbose_name_plural = _('Contacts')

    def __str__(self):
        return self.title


class ExamEvent(models.Model):
    title = models.CharField(_('Title'), max_length=255)
    start = models.DateTimeField(_('Start'), db_index=True)
    address = models.CharField(_('Address'), max_length=255, blank=True)
    description = models.TextField(_('Description'), blank=True)
    submitted = models.BooleanField(_('Submitted'))
    registration = models.ForeignKey(
        'RegistrationEvent',
        on_delete=models.CASCADE,
        verbose_name=_('Registration'))

    class Meta:
        verbose_name = _('Exam')
        verbose_name_plural = _('Exams')

    def __str__(self):
        return self.title


class Attached(models.Model):
    title = models.CharField(_('Title'), max_length=255)
    registration = models.ForeignKey(
        'RegistrationEvent', on_delete=models.CASCADE)
    document = models.FileField(
        _('Documents'), upload_to="documents", null=True, blank=True)

    class Meta:
        verbose_name = _('Attachment')
        verbose_name_plural = _('Attachments')

    def __str__(self):
        return self.title


class RegistrationEvent(models.Model):
    start = models.DateTimeField(
        _('Start'), db_index=True, blank=True, null=True)
    end = models.DateTimeField(
        _('Deadline'), db_index=True, blank=True, null=True)
    title = models.CharField(_('Firm'), max_length=255)
    address = models.CharField(_('Address'), max_length=255, blank=True)
    description = models.TextField(_('Description'), blank=True)
    website = models.URLField(blank=True)
    submitted = models.BooleanField(_('Submitted'))
    cost = models.FloatField(_('Cost'), blank=True, null=True)

    class Meta:
        verbose_name = _('Registration')
        verbose_name_plural = _('Registrations')

    def __str__(self):
        return self.title
