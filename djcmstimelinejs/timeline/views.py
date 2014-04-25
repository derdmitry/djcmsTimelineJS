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
        elif isinstance(obj, datetime.timedelta):
            return (datetime.datetime.min + obj).time().isoformat()
        else:
            return super(DateTimeEncoder, self).default(obj)


def get_json(request):
    cat_ids = request.GET.getlist('cat_ids[]', [])
    tl = Timeline.objects.last()
    result = {
        "timeline":{
            "type": tl.type,
            "text": tl.text,
            "headline": tl.headline,
            "startDate": tl.startDate,
            "date":[]
        }
    }

    if cat_ids:
        dates = tl.date.filter(category_id__in=map(int, cat_ids))
    else:
        dates = tl.date.all()

    for date in dates:
        result["timeline"]['date'].append(model_to_dict(date))

    return HttpResponse(json.dumps(result, cls=DateTimeEncoder))
