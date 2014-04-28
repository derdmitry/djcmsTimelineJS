from django.conf.urls import patterns, include, url
from timeline.views import TimelineList, TimelienDetail

urlpatterns = patterns(
    'timeline.views',
    url(r'^timeline/$', TimelineList.as_view()),
    url(r'^timeline/(?P<pk>[0-9]+)/$', TimelienDetail.as_view()),

)
