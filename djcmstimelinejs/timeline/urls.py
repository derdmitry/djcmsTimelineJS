from django.conf.urls import patterns, include, url


urlpatterns = patterns(
    'timeline.views',
    url(r'get_json', 'get_json', name='get_json'),

)
