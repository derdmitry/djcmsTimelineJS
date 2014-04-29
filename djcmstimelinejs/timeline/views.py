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

    def get_serializer(self, instance=None, data=None,
                       files=None, many=False, partial=False):
        serializer_class = self.get_serializer_class()
        context = self.get_serializer_context()
        cat_ids = self.request.GET.getlist('cat_ids[]', [])
        context["cat_ids"] = cat_ids
        return serializer_class(instance, data=data, files=files,
                                many=many, partial=partial, context=context)
