from django.conf.urls.defaults import *

urlpatterns = patterns('forum.views',
    url(r'^$','index'),
    url(r'^(?P<forum_name>[\w\s]+)/$','viewForum'),
    url(r'^(?P<forum_name>[\w\s]+)/(?P<thread_name>[\w\s]+)/$','viewThread')
)