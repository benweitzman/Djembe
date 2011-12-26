from django.conf.urls.defaults import *

urlpatterns = patterns('forum.views',
    url(r'^$','index'),
    url(r'^forum/(?P<forum_id>\d+)/$','viewForum'),
    url(r'^post/(?P<post_id>\d+)/$','viewPost'),
    #url(r'[\w\s]+/[\w\s]+/reply/(?P<post_id>[\d]+)/$','viewPost'),
    url(r'^thread/(?P<thread_id>\d+)/$','viewThread'),
    url(r'^thread/(?P<thread_id>\d+)/(?P<page>\d+)/$','viewThread')
)