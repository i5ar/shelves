from __future__ import absolute_import, unicode_literals

from django.conf import settings
from django.conf.urls import include, url
from django.contrib import admin
from django.conf.urls.i18n import i18n_patterns

from search import views as search_views

from wagtail.wagtailadmin import urls as wagtailadmin_urls
from wagtail.wagtailcore import urls as wagtail_urls
from wagtail.wagtaildocs import urls as wagtaildocs_urls

from rest_framework_jwt.views import obtain_jwt_token, verify_jwt_token

from accounts.views import MemberRegistrationView
from shelves import urls as shelves_urls
from portables import urls as portables_urls
from diaries import urls as diaries_urls


urlpatterns = i18n_patterns(
    url(r'^django-admin/', include(admin.site.urls)),

    url(r'^admin/', include(wagtailadmin_urls)),
    url(r'^documents/', include(wagtaildocs_urls)),

    # NOTE: Schedule
    url(r'^schedule/', include('schedule.urls', namespace='schedule')),

    # NOTE: Restframework
    url(r'^api/snippets/', include('snippets.urls')),
    url(r'^api/shelves/', include(
        'shelves.api.urls', namespace='shelves-api')),
    url(r'^api/accounts/', include(
        'accounts.api.urls', namespace='accounts-api')),
    url(r'^api-auth/', include(
        'rest_framework.urls', namespace='rest_framework')),
    # JWT
    url(r'^api-token-auth/', obtain_jwt_token),
    url(r'^api-token-verify/', verify_jwt_token),

    # https://docs.djangoproject.com/en/1.9/topics/i18n/translation/#the-set-language-redirect-view
    url(r'^i18n/', include('django.conf.urls.i18n')),

    # NOTE: Registration
    # https://django-registration-redux.readthedocs.io/en/latest/quickstart.html
    url(r'^accounts/register/$',
        MemberRegistrationView.as_view(),
        name='registration_register'),
    url(r'^accounts/', include('registration.backends.default.urls')),

    # NOTE: Profile
    url(r'^accounts/profile/', include('accounts.urls', namespace='profile')),

    # NOTE: Shelves
    url(r'^shelves/', include(shelves_urls, namespace='shelves')),

    # NOTE: Portables
    url(r'^portables/', include(portables_urls)),
    # NOTE: Diaries
    url(r'^diaries/', include(diaries_urls, namespace='diaries')),

    url(r'^search/$', search_views.search, name='search'),

    # For anything not caught by a more specific rule above, hand over to
    # Wagtail's page serving mechanism. This should be the last pattern in
    # the list:
    url(r'', include(wagtail_urls)),

    # Alternatively, if you want Wagtail pages to be served from a subpath
    # of your site, rather than the site root:
    #    url(r'^pages/', include(wagtail_urls)),
)


if settings.DEBUG:
    from django.conf.urls.static import static
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns

    # Serve static and media files from development server
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
