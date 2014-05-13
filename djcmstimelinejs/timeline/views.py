from models import Timeline
from timeline.serializers import TimelineSerializer
from rest_framework import generics
from rest_framework.renderers import BrowsableAPIRenderer
from timeline.utils import CustomJSONRenderer
from datetime import datetime


class TimelineList(generics.ListCreateAPIView):
    queryset = Timeline.objects.all()
    serializer_class = TimelineSerializer


class TimelineDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Timeline.objects.all()
    serializer_class = TimelineSerializer
    renderer_classes = [BrowsableAPIRenderer, CustomJSONRenderer]

    def get_serializer_context(self):
        context = super(TimelineDetail, self).get_serializer_context()
        context["cat_ids"] = self.request.GET.getlist('cat_ids[]', [])
        context["page"] = int(self.request.GET.get('page', 1))
        context["count"] = int(self.request.GET.get('count', 3))
        start_date = self.request.GET.get('start_date', None)

        if start_date:
            context["start_date"] = datetime.strptime(start_date, '%Y-%m-%d')
        end_date = self.request.GET.get('end_date', None)
        if end_date:
            context["end_date"] = datetime.strptime(end_date, '%Y-%m-%d')

        return context
