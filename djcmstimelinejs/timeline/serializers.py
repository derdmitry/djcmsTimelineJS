from rest_framework import serializers
from timeline import models as tm
from django.db.models.base import ModelBase
from django.db import models
import sys


class TimelineSerializer(serializers.ModelSerializer):

    date = serializers.SerializerMethodField('get_dates')

    def get_dates(self,obj):
        categories_id = self.context.get('cat_ids', None)
        if categories_id:
            dates = obj.date.filter(category_id__in=categories_id)
        else:
            dates = obj.date.all()
        return DateSerializer(dates).data

    class Meta:
        model= tm.Timeline
        resource_name = 'timeline'


class AssetSerializer(serializers.ModelSerializer):

    class Meta:
        model= tm.Asset


class DateSerializer(serializers.ModelSerializer):
    asset = AssetSerializer(source='asset')
    startDate = serializers.DateTimeField(format='%Y,%m,%d')
    endDate = serializers.DateTimeField(format='%Y,%m,%d')

    class Meta:
        model= tm.Date


class BaseSerializer(serializers.ModelSerializer):
    def __init__(self, classtype, *arg, **kwargs):
        self._type = classtype


def ClassFactory(name, argnames, BaseSerializer=BaseSerializer):
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            if key not in argnames:
                raise TypeError("Argument %s not valid for %s"
                                % (key, self.__class__.__name__))
            setattr(self, key, value)
        return BaseSerializer.__init__(self, name[:-len("Class")])

    class Meta:
        pass

    attrs = {'__init__': __init__,
             '__module__': sys.modules[__name__],
             'Meta': Meta}
    newclass = type(name, (BaseSerializer, ), attrs)
    return newclass


def SerializerFactory(name, model, args={}, BaseSerializer=serializers.ModelSerializer):
    class Meta:
        pass
    Meta.model = model
    newserializer = type(name, (BaseSerializer, ), args)
    newserializer.Meta = Meta
    return newserializer


# if '__all__' in dir(tm):
#     models = filter(lambda x: x[0] in tm.__all__, tm.__dict__.items())
# else:
#     models = tm.__dict__.items()
# for name, var in models:
#     if type(var) is ModelBase:
#         kwa = dict(
#             [(x.name, serializers.__dict__.get(x.__class__.__name__, serializers.Field).__call__()) for x in var._meta.fields])
#         tempClass = SerializerFactory("%sSerializer" % name, var)
#         setattr(sys.modules[__name__], "%sSerializer" % name, tempClass)


