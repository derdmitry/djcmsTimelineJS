from rest_framework import serializers
from timeline import models as tm
import datetime
import sys
import  math

class TimelineSerializer(serializers.ModelSerializer):

    date = serializers.SerializerMethodField('get_dates')
    date_count = serializers.SerializerMethodField('get_date_count')
    current_page = serializers.SerializerMethodField('get_page')
    total_page = serializers.SerializerMethodField('get_total_page')
    start_date = serializers.SerializerMethodField('get_start_date')
    end_date = serializers.SerializerMethodField('get_end_date')

    def get_dates(self,obj):
        categories_id = self.context.get('cat_ids', None)
        page = self.context.get('page', 1)
        count = self.context.get('count', 3)
        start_date = self.context.get("start_date", None)
        end_date = self.context.get("end_date", None)
        if categories_id:
            dates = obj.date.filter(category_id__in=categories_id)
        else:
            dates = obj.date.all()
        if start_date and end_date:
            dates = dates.filter(startDate__range=(start_date, end_date))

        return DateSerializer(dates[page*count:page*count+count]).data

        #return DateSerializer(dates).data

    def get_date_count(self, obj):
        categories_id = self.context.get('cat_ids', None)
        if categories_id:
            return obj.date.filter(category_id__in=categories_id).count()
        else:
            return obj.date.count()

    def get_page(self, obj):
        return self.context.get('page', 1)

    def get_total_page(self, obj):
        count = self.context.get('count', 3)
        categories_id = self.context.get('cat_ids', None)
        if categories_id:
            date_count = obj.date.filter(category_id__in=categories_id).count()
        else:
            date_count = obj.date.count()
        return int(math.ceil(date_count/float(count)))

    def get_start_date(self, obj):
        categories_id = self.context.get('cat_ids', None)
        date = obj.date.filter(category_id__in=categories_id).order_by("startDate").first()
        print date
        if date:
            return date.startDate
        else:
            d = datetime.datetime.now()
            return datetime.date(d.year, d.month, d.day)

    def get_end_date(self, obj):
        categories_id = self.context.get('cat_ids', None)
        date = obj.date.filter(category_id__in=categories_id).order_by("-endDate").first()
        if date:
            return date.endDate
        else:
            d = datetime.datetime.now()

            return datetime.date(d.year, d.month, d.day)

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


