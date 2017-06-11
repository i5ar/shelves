from __future__ import absolute_import, unicode_literals

from django.db import models

from modelcluster.fields import ParentalKey

from wagtail.wagtaildocs.models import AbstractDocument
from wagtail.wagtailcore.models import Page, Orderable
from wagtail.wagtailcore.fields import RichTextField
from wagtail.wagtailadmin.edit_handlers import FieldPanel, InlinePanel
from wagtail.wagtailimages.edit_handlers import ImageChooserPanel
from wagtail.wagtaildocs.edit_handlers import DocumentChooserPanel
from wagtail.wagtailsearch import index
from wagtail.wagtailsnippets.models import register_snippet

import os


class HomePage(Page):
    pass


class DocsPage(Page):
    date = models.DateField("Post date", blank=True, null=True)
    intro = models.CharField(max_length=250, blank=True)
    body = RichTextField(blank=True)


    # def events(self):
    #     # Get list of live event pages that are descendants of this page
    #     events = DocsPage.objects.live().descendant_of(self)
    #     return events.first().title

    # http://stackoverflow.com/questions/5135556/dynamic-file-path-in-django
    def get_upload_path(instance, filename):
        # return os.path.join(
        #   "%s" % instance.intro, "%s" % instance.get_parent(), filename)
        mylist = []
        for i in instance.get_ancestors():
            mylist.append(i.title)
        mylist.append(filename)
        mylist = mylist[2:]
        return os.path.join(*mylist)

    document_custom = models.FileField(
        null=True,
        blank=True,
        # upload_to='document_custom/',
        upload_to=get_upload_path,
        verbose_name='document_custom'
    )

    search_fields = Page.search_fields + [
        index.SearchField('intro'),
        index.SearchField('body'),
    ]

    content_panels = Page.content_panels + [
        FieldPanel('date'),
        FieldPanel('intro'),
        FieldPanel('body', classname="full"),
        FieldPanel('document_custom'),
        InlinePanel('gallery_docs', label="Gallery docs"),
    ]

class DocsPageGalleryDocument(Orderable):
    page = ParentalKey(DocsPage, related_name='gallery_docs')
    document = models.ForeignKey(
        'wagtaildocs.Document',
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name='+'
    )
    caption = models.CharField(blank=True, max_length=250)
    panels = [
        DocumentChooserPanel('document'),
        FieldPanel('caption'),
    ]
