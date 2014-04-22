from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render
from django.views.generic import ListView
from django.views.generic.list import MultipleObjectMixin
from django.http import Http404
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