from django.contrib.auth import get_user_model
from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import Group

from registration import signals
from registration.models import RegistrationProfile

from rest_framework import serializers

from ..models import Member

UserModel = get_user_model()


class UserSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = UserModel
        fields = (
            'url', 'id', 'username', 'first_name', 'last_name', 'email')
        # http://www.django-rest-framework.org/topics/3.0-announcement/#changes-to-hyperlinkedmodelserializer
        extra_kwargs = {
            'url': {'view_name': "accounts-api:user-detail"},
        }


class MemberSerializer(serializers.HyperlinkedModelSerializer):

    username = serializers.SerializerMethodField()

    def get_username(self, obj):
        return obj.user.username

    password = serializers.SerializerMethodField()

    def get_password(self, obj):
        return obj.user.password

    password2 = serializers.SerializerMethodField()

    def get_password2(self, obj):
        return obj.user.password

    email = serializers.SerializerMethodField()

    def get_email(self, obj):
        return obj.user.email

    class Meta:
        model = Member
        fields = (
            'url',  'username', 'email', 'password', 'password2', 'membership')
        # http://www.django-rest-framework.org/topics/3.0-announcement/#changes-to-hyperlinkedmodelserializer
        extra_kwargs = {
            'url': {'view_name': "accounts-api:member-detail"},
        }


# TODO: Get messages from django-registration-redux
password_error_match = _("Password must match.")
email_error_exist = _(
    "This email address is already in use. " +
    "Please supply a different email address."
)


class UserCreateSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(label=_('Email Address'))
    password2 = serializers.CharField(
        label=_('Confirm Password'),
        write_only=True,
        style={'input_type': 'password'})

    class Meta:
        model = UserModel
        fields = [
            'username',
            'email',
            'password',
            'password2',
        ]
        extra_kwargs = {
            "password": {
                "write_only": True,
                "style": {'input_type': 'password'}
            }
        }

    # NOTE: This serializer is nested below so the validators must be removed.
    # http://www.django-rest-framework.org/api-guide/validators/#updating-nested-serializers
    '''
    def validate_email(self, data):
        """Check unique email via queryset."""
        email = data
        user_qs = UserModel.objects.filter(email=email)
        if user_qs.exists():
            raise serializers.ValidationError(email_error_exist)

        return data

    def validate_password(self, data):
        initial_data = self.get_initial()
        password2 = initial_data.get("password2")
        password = data
        if password != password2:
            raise serializers.ValidationError(password_error_match)
        return data

    def validate_password2(self, data):
        initial_data = self.get_initial()
        password = initial_data.get("password")
        password2 = data
        if password != password2:
            raise serializers.ValidationError(password_error_match)
        return data

    def create(self, validated_data):
        username = validated_data['username']
        email = validated_data['email']
        password = validated_data['password']
        user = UserModel(username=username, email=email)
        user.set_password(password)
        user.save()
        return validated_data
    '''


class MemberCreateSerializer(serializers.ModelSerializer):
    """Nest UserCreateSerializer to add membership field from Member model.

    .. Nested serializer:
        https://stackoverflow.com/questions/39781625/

    """

    # NOTE: User serializer name used by the front-end.
    userial = UserCreateSerializer()

    class Meta:
        model = Member
        fields = [
            'userial',
            'membership',
        ]

    def validate(self, data):
        initial_data = self.get_initial()
        userserializer_data = initial_data.get("userial")
        email = userserializer_data['email']
        password = userserializer_data['password']
        password2 = userserializer_data['password2']

        # Check unique email via queryset.
        user_qs = UserModel.objects.filter(email=email)
        if user_qs.exists():
            raise serializers.ValidationError(email_error_exist)

        # Confirm password.
        if password != password2:
            raise serializers.ValidationError(password_error_match)

        return data

    # NOTE: Get registration-redux settings
    SEND_ACTIVATION_EMAIL = getattr(settings, 'SEND_ACTIVATION_EMAIL', True)
    registration_profile = RegistrationProfile

    def create(self, validated_data):

        model_data = validated_data['userial']
        username = model_data["username"]
        email = model_data["email"]
        password = model_data["password"]

        # NOTE: Create a registration profile using registration-redux
        site = get_current_site(self.context.get('request'))

        new_user_instance = UserModel.objects.create_user(
            username=username, email=email, password=password)
        new_user_instance.save()

        new_user = self.registration_profile.objects.create_inactive_user(
            new_user=new_user_instance,
            site=site,
            send_email=self.SEND_ACTIVATION_EMAIL,
            request=self.context.get('request'),
        )

        signals.user_registered.send(
            sender=self.__class__,
            user=new_user,
            request=self.context.get('request'))

        # NOTE: Add membership attribute
        member = Member.objects.create(
            user=new_user,
            membership=validated_data['membership'],
        )
        member.save()

        # NOTE: Add user to group
        group, created = Group.objects.get_or_create(name='Member')
        group.user_set.add(new_user)

        return validated_data


class UserLoginSerializer(serializers.ModelSerializer):
    token = serializers.CharField(allow_blank=True, read_only=True)
    username = serializers.CharField()
    email = serializers.EmailField(label='Email Address')

    class Meta:
        model = UserModel
        fields = [
            'username',
            'email',
            'password',
            'token',
        ]
        extra_kwargs = {"password": {"write_only": True}}
