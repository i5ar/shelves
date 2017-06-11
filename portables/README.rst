=========
Portables
=========

Portables is a simple PDF generator

Requirements
------------

- `ReportLab <http://www.reportlab.com/opensource/>`_ require PIL or Pillow with Freetype support:

    There are no absolute prerequisites beyond the Python standard library;
    but the Python Imaging Library (PIL or Pillow) is needed to include images other than JPG inside PDF files.

So you must install::

    yum install libjpeg-turbo-devel libjpeg-turbo-devel libpng-devel freetype-devel

- Require Flat pages and SITE_ID in settings:

    1. Install the `sites framework <https://docs.djangoproject.com/en/1.8/ref/contrib/sites/#module-django.contrib.sites>`_ by adding :code:`django.contrib.sites` to your :code:`INSTALLED_APPS` setting, if it’s not already in there. Also make sure you’ve correctly set :code:`SITE_ID` to the ID of the site the settings file represents.

    2. Add :code:`django.contrib.flatpages` to your :code:`INSTALLED_APPS` setting.

Here how it looks::

    INSTALLED_APPS = (
        ...
        'django.contrib.admin',
        'django.contrib.sites', # flatpages
        'django.contrib.flatpages', # flatpages
        ...
    )

    SITE_ID = 1

Quick start
-----------

1. Add "portables" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = (
        ...
        'portables',
    )

2. Include the portables URLconf in your project urls.py like this::

    url(r'^pdf/', include('portables.urls')),

3. Run `python manage.py migrate` to create the polls models.

4. Start the development server and visit http://127.0.0.1:8000/admin/
   to create a PDF (you'll need the Admin app enabled).

5. Visit http://127.0.0.1:8000/pdf/ to use in the PDF generator.
