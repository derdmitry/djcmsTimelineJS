from django.http import HttpResponse
from django.core import serializers
from models import Timeline, model_to_dict
from django.core.serializers.json import DjangoJSONEncoder
import json
import datetime


class DateTimeEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.isoformat()
        elif isinstance(obj, datetime.date):
            return obj.strftime('%Y,%m,%d')
            #return obj.isoformat()
        elif isinstance(obj, datetime.timedelta):
            return (datetime.datetime.min + obj).time().isoformat()
        else:
            return super(DateTimeEncoder, self).default(obj)


# class TimelineList(ListView):
#
#     model = Timeline
#
#     def get(self, request, *args, **kwargs):
#         self.object_list = self.get_queryset()
#         allow_empty = self.get_allow_empty()
#         return "ok"#serializers.serialize('json', self.object_list)

def get_json(request):
    object_list = Timeline.objects.all()
    result = []
    for obj in object_list:
        result.append({obj.__class__.__name__.lower():model_to_dict(obj)})

    return HttpResponse(json.dumps({'timeline':model_to_dict(Timeline.objects.first())},
                                   cls=DateTimeEncoder))