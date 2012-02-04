from django.conf.urls.defaults import *

urlpatterns = patterns('ajax.views',
    url(r'^$','index'),
    url(r'^unique/$','checkUnique'),
    url(r'^previewpost/$','postPreview'),
    url(r'^editpost/$','editPost'),
    url(r'^getIds/$','getIds'),
)