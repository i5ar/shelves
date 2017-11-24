from django import forms
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User

from registration.forms import RegistrationForm

from .models import MEMBERSHIP_CHOICES, Biography


# TODO: Use RegistrationFormUniqueEmail
class MemberRegistrationForm(RegistrationForm):
    '''Member fields'''
    membership = forms.ChoiceField(
        label=_('Membership'),
        choices=MEMBERSHIP_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    def __init__(self, *args, **kwargs):
        super(MemberRegistrationForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget = forms.TextInput(
            attrs={'class': 'form-control'})
        self.fields['email'].widget = forms.TextInput(
            attrs={'class': 'form-control'})
        self.fields['password1'].widget = forms.TextInput(
            attrs={'class': 'form-control', 'type': 'password'})
        self.fields['password2'].widget = forms.TextInput(
            attrs={'class': 'form-control', 'type': 'password'})

    def clean_username(self):
        '''Registration incasesensitive user names'''
        if User.objects.filter(
            username__iexact=self.cleaned_data['username'].lower()
        ).count():
            # Validation error
            # https://docs.djangoproject.com/en/1.8/ref/exceptions/#validationerror
            raise forms.ValidationError(
                _('A user with that username already exists.'))
        return self.cleaned_data['username']


class UserForm(forms.ModelForm):
    """User"""
    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name')


class BiographyForm(forms.ModelForm):
    """Profile"""
    class Meta:
        model = Biography
        fields = ('gender', 'gender_visible')
