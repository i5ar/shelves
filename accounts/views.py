from django.shortcuts import render
from django.contrib.auth.models import Group
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.urls import reverse

from registration.backends.default.views import RegistrationView
from registration.forms import RegistrationFormUniqueEmail

from .forms import MemberRegistrationForm, BiographyForm, UserForm
from .models import Membership


# Registration views
# http://django-registration.readthedocs.org/en/latest/views.html
class RegistrationViewUniqueEmail(RegistrationView):
    '''Force Unique Email Registration Form'''
    form_class = RegistrationFormUniqueEmail


# http://stackoverflow.com/questions/29620940/django-registration-redux-add-extra-field/
class MemberRegistrationView(RegistrationView):

    form_class = MemberRegistrationForm

    def register(self, form_class):
        r_user = super(MemberRegistrationView, self).register(form_class)

        r_profile = Membership.objects.create(
                user=r_user,
                membership=form_class.cleaned_data['membership'],
        )

        r_profile.save()

        # NOTE: Add user to group
        group, created = Group.objects.get_or_create(name='Member')
        group.user_set.add(r_user)

        return r_user


@login_required
def index(request):
    member = get_object_or_404(Membership, user_id=request.user)
    context = {'member': member}
    return render(request, 'accounts/profile.html', context)


@login_required
def edit(request):
    '''
    Update all profile fields.
    '''
    # NOTE: More forms in a page require specific URL in the form action.
    try:
        form_biography = BiographyForm(instance=request.user.biography)
        form_user = UserForm(instance=request.user)
    except:
        form_biography = BiographyForm
        form_user = UserForm

    context = {
        'form_biography': form_biography,
        'form_user': form_user
    }

    # Render
    # https://docs.djangoproject.com/en/1.8/topics/http/shortcuts/#render
    # return render_to_response(
    #     'accounts/jumbotron-edit.html',
    #     context,
    #     context_instance=RequestContext(request))
    return render(request, 'accounts/edit.html', context)


@login_required
def edit_user(request):
    '''Update User Field'''
    if request.method == 'POST':
        form_user = UserForm(
            request.POST, instance=request.user)
        if form_user.is_valid():
            form_user.save()
            return HttpResponseRedirect(reverse('profile:index'))
    else:
        try:
            form_user = UserForm(instance=request.user)
        except:
            form_user = UserForm

    context = {'form_user': form_user}

    return render(request, 'accounts/edit.html', context)


@login_required
def edit_biography(request):
    '''Update Biography Field'''
    if request.method == 'POST':
        form_biography = BiographyForm(
            request.POST, instance=request.user.biography)
        if form_biography.is_valid():
            form_biography.save()
            return HttpResponseRedirect(reverse('profile:index'))
    else:
        try:
            form_biography = BiographyForm(instance=request.user.biography)
        except:
            form_biography = BiographyForm

    context = {'form_biography': form_biography}

    return render(request, 'accounts/edit.html', context)


def detail(request, username):
    '''Get objects from database'''
    user_id = get_object_or_404(User, username=username).pk
    member = get_object_or_404(Membership, user_id=user_id)
    context = {'member': member}
    return render(request, 'accounts/detail.html', context)
