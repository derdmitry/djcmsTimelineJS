from django.http import HttpResponse
from django.core import serializers
from models import Timeline


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
    return HttpResponse(serializers.serialize('json', object_list))