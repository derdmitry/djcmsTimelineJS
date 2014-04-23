from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ObjectDoesNotExist

from cms.models import CMSPlugin
# Create your models here.


class News(CMSPlugin):
    title = models.CharField(max_length=100)
    show_title = models.BooleanField(default=True)

    class Meta:
        verbose_name=_('News CMS Plugin')

    def __unicode__(self):
        return self.title


class Category(models.Model):
    name = models.CharField(max_length=32)

    def __unicode__(self):
        return self.name


class AssetManager(models.Manager):
    def get_by_natural_key(self, caption, credit, media):
        return self.get(caption=caption, credit=credit, media=media)


class Asset(models.Model):

    media = models.URLField()
    credit = models.CharField(max_length=100)
    caption = models.CharField(max_length=100)
    objects = AssetManager()

    def __unicode__(self):
        return self.caption

    def natural_key(self):
        return (self.caption,
                self.credit,
                self.media)


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

    def natural_key(self):
        return (self.name,
                self.headline,
                self.text,
                self.startDate,
                self.endDate,
                self.tag,
                self.classname) + self.asset.natural_key()


class Timeline(models.Model):

    type = models.CharField(max_length=32)
    text = models.CharField(max_length=255)
    headline = models.CharField(max_length=100)
    startDate = models.DateField()
    date = models.ManyToManyField(Date, verbose_name='date')

    def __unicode__(self):
        return self.headline


def model_to_dict(obj, exclude=('AutoField',  'OneToOneField')):
    tree = {}
    exclude = set(exclude)
    for field_name in obj._meta.get_all_field_names():

        try:
            field = getattr(obj, field_name)
        except (ObjectDoesNotExist, AttributeError):
            continue
        #print obj, field_name
        #import pdb;pdb.set_trace()
        if field.__class__.__name__ in ['RelatedManager', 'ManyRelatedManager', 'ForeignKey']:
            if field.model.__name__ in exclude:
                continue

            if field.__class__.__name__ == 'ManyRelatedManager':
                #import pdb;pdb.set_trace()
                exclude.add(obj.__class__.__name__)

            subtree = []

            for related_obj in getattr(obj, field_name).all():
                value = model_to_dict(related_obj, exclude=exclude)
                if value:
                    subtree.append(value)
            if subtree:
                tree[field_name] = subtree
            continue

        field = obj._meta.get_field_by_name(field_name)[0]
        if field.__class__.__name__ in exclude:
            continue

        if field.__class__.__name__ == 'RelatedObject':
            exclude.add(field.model.__name__)
            #print field_name, getattr(obj, field_name)
            tree[field_name] = model_to_dict(getattr(obj, field_name), exclude=exclude)
            continue

        if field.__class__.__name__ == 'ForeignKey'and getattr(obj, field_name):

            value = model_to_dict(getattr(obj, field_name), exclude)
        else:
            value = getattr(obj, field_name)

        if value:
            tree[field_name] = value

    return tree