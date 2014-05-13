from django.conf.urls import patterns, include, url
from timeline.views import TimelineList, TimelineDetail

urlpatterns = patterns(
    'timeline.views',
    url(r'^timeline/$', TimelineList.as_view()),
    url(r'^timeline/(?P<pk>[0-9]+)/$', TimelineDetail.as_view()),

)
