from django.conf.urls.defaults import *

urlpatterns = patterns('plugins.movies.views',
    url(r'^films/$', 'filmsIndex'),
    url(r'^films/(?P<film_id>\d+)/$','filmPage'),
    url(r'^people/$','peopleIndex'),
)