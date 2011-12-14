from django.conf.urls.defaults import *

urlpatterns = patterns('ajax.views',
    (r'^$','index'),
)