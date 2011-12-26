from django.conf.urls.defaults import *

urlpatterns = patterns('tracker.views',
                       url(r'^(?P<key>\w+)/announce/$','announce'),
                       )