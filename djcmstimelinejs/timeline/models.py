from django.db import models
from django.utils.translation import gettext_lazy as _

from cms.models import CMSPlugin
# Create your models here.

class News(CMSPlugin):
    title = models.CharField(max_length=100)
    show_title = models.BooleanField(default=True)

    class Meta:
        verbose_name=_('News CMS Plugin')

    def __unicode__(self):
        return self.title


class Asset(models.Model):

    media = models.URLField()
    credit = models.CharField(max_length=100)
    caption = models.CharField(max_length=100)


class Item(models.Model):

    name = models.CharField(max_length=32)
    headline = models.CharField(max_length=100)
    text = models.CharField(max_length=255)
    start_date = models.DateField()
    end_date = models.DateField()
    tag = models.CharField(max_length=255)
    classname = models.CharField(max_length=100)
    asset = models.ForeignKey(Asset)


class Timeline(models.Model):

    type = models.CharField(max_length=32)
    text = models.CharField(max_length=255)
    headline = models.CharField(max_length=100)
    items = models.ManyToManyField(Item)
