from models import Timeline
from timeline.serializers import TimelineSerializer
from rest_framework import generics
from rest_framework.renderers import BrowsableAPIRenderer
from timeline.utils import CustomJSONRenderer


class TimelineList(generics.ListCreateAPIView):
    queryset = Timeline.objects.all()
    serializer_class = TimelineSerializer


class TimelienDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Timeline.objects.all()
    serializer_class = TimelineSerializer
    renderer_classes = [BrowsableAPIRenderer, CustomJSONRenderer]

    def get_serializer_context(self):
        context = super(TimelienDetail, self).get_serializer_context()
        context["cat_ids"] = self.request.GET.getlist('cat_ids[]', [])
        context["page"] = int(self.request.GET.get('page', 1))
        context["count"] = int(self.request.GET.get('count', 3))
        return context
