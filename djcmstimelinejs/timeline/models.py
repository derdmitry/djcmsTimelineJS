from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ObjectDoesNotExist
from cms.models import CMSPlugin

#__all__ = ['Category',]


class Category(models.Model):
    name = models.CharField(max_length=32)

    def __unicode__(self):
        return self.name


class Asset(models.Model):

    media = models.URLField()
    credit = models.CharField(max_length=100)
    caption = models.CharField(max_length=100)

    def __unicode__(self):
        return self.caption


class Date(models.Model):

    name = models.CharField(max_length=32)
    headline = models.CharField(max_length=100)
    text = models.CharField(max_length=255)
    startDate = models.DateField()
    endDate = models.DateField()
    tag = models.CharField(max_length=255)
    classname = models.CharField(max_length=100)
    asset = models.ForeignKey(Asset)
    category = models.ForeignKey(Category, blank=True, null=True)

    def __unicode__(self):

        return self.name


class Timeline(models.Model):

    type = models.CharField(max_length=32)
    text = models.CharField(max_length=255)
    headline = models.CharField(max_length=100)
    startDate = models.DateField()
    date = models.ManyToManyField(Date, verbose_name='date')

    def __unicode__(self):
        return self.headline


class News(CMSPlugin):
    title = models.CharField(max_length=100)
    timeline = models.ForeignKey(Timeline, related_name='plugins',
        blank=True, null=True)

    class Meta:
        verbose_name = _('News CMS Plugin')

    def __unicode__(self):
        return self.title
