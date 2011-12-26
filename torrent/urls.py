from django.conf.urls.defaults import *

urlpatterns = patterns('torrent.views',
                       url(r'^$','index'),
                       url(r'^get/(?P<id>\d+)/$','get'),
                       url(r'^upload/$','upload'),
                       )