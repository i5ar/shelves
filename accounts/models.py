from django.db import models
from django.db.models.signals import post_save
from django.utils.translation import ugettext_lazy as _
from django.dispatch import receiver
from django.contrib.auth.models import User

# Referencing User model
# https://docs.djangoproject.com/en/1.10/topics/auth/customizing/#referencing-the-user-model
# from django.contrib.auth import get_user_model
# User = get_user_model()

# NOTE: Used by Member model and MemberRegistrationForm
MEMBERSHIP_CHOICES = (
    ('', ''),
    ('free', _('Free')),
    ('pro', _('Professional')),
)


class Member(models.Model):
    """Registered User with Membership."""
    # Existing User model
    # https://docs.djangoproject.com/en/1.8/topics/auth/customizing/#extending-the-existing-user-model
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # https://docs.djangoproject.com/en/1.8/ref/models/fields/#choices
    membership = models.CharField(
        _('Membership'), max_length=16, choices=MEMBERSHIP_CHOICES)

    class Meta:
        ordering = ['membership']
        verbose_name = 'Membership'
        verbose_name_plural = 'Memberships'

    def __str__(self):
        return self.membership


class Biography(models.Model):
    """User Additional Info."""
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # https://docs.djangoproject.com/en/1.8/ref/models/fields/#choices
    MALE = 'M'
    FEMALE = 'F'
    GENDER_CHOICES = (
        ('', ''),
        (MALE, _('Male')),
        (FEMALE, _('Female')),
    )
    gender = models.CharField(
        max_length=1, choices=GENDER_CHOICES, default='')
    gender_visible = models.BooleanField(default=0)

    def __str__(self):
        return self.user.username


# NOTE: Lambda function get or create biography profile on model access
# User.biography = property(
#     lambda u: Biography.objects.get_or_create(user=u)[0])

# NOTE: Signals create biography profile on user creation
@receiver(post_save, sender=User)
def add_biography_profile(sender, **kwargs):
    if kwargs.get('created', False):
        Biography.objects.create(user=kwargs.get('instance'))
