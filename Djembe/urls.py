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

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$','Djembe.views.index'),
    url(r'^artists/$','groups.views.artistsIndex'),
    url(r'^artists/(?P<artist_name>[\w]+)/$','groups.views.artistPage'),
    url(r'^albums/(?P<album_name>[\w\s]+)/$','groups.views.albumPage'),
    url(r'^albums/(?P<album_name>[\w\s]+)/addtag/$','groups.views.addTag'),
    url(r'^ajax/',include('ajax.urls')),
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root':settings.MEDIA_ROOT}),
)
