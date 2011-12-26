from django.conf import settings
from django.conf.urls import patterns, include, url
from django.contrib import admin
admin.autodiscover()
# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'Djembe.views.home', name='home'),
    # url(r'^Djembe/', include('Djembe.foo.urls')),

    url(r'^tracker/',include('tracker.urls')),

    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$','Djembe.views.index'),
    url(r'^artists/$','groups.views.artistsIndex'),
    url(r'^artists/(?P<artist_name>[\w]+)/$','groups.views.artistPage'),
    url(r'^albums/(?P<album_name>[\w\s]+)/$','groups.views.albumPage'),
    url(r'^albums/(?P<album_name>[\w\s]+)/addtag/$','groups.views.addTag'),
    url(r'^ajax/',include('ajax.urls')),
    url(r'^profile/',include('userprofile.urls')),
    url(r'^user/$','userprofile.views.view'),
    url(r'^users/(?P<username>[\w]+)','userprofile.views.view'),
    url(r'^accounts/', include('registration.urls')),
    url(r'^forums/',include('forum.urls')),
    url(r'^torrent/',include('torrent.urls')),
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root':settings.MEDIA_ROOT}),
)
