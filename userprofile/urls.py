from django.conf.urls.defaults import *

urlpatterns = patterns('userprofile.views',
    url(r'^mine/$','mine'),
    url(r'^edit/$','editProfile'),
)