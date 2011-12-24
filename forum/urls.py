from django.conf.urls.defaults import *

urlpatterns = patterns('forum.views',
    url(r'^$','index'),
    url(r'^(?P<forum_name>[\w\s]+)/$','viewForum'),
    url(r'^post=(?P<post_id>[\d]+)/$','viewPost'),
    url(r'[\w\s]+/[\w\s]+/reply/(?P<post_id>[\d]+)/$','viewPost'),
    url(r'^(?P<forum_name>[\w\s]+)/(?P<thread_name>[\w\s]+)/$','viewThread'),
    url(r'^(?P<forum_name>[\w\s]+)/(?P<thread_name>[\w\s]+)/(?P<page>[\d]+)/$','viewThread')
)