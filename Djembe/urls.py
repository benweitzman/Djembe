from django.conf import settings
from django.conf.urls import patterns, include, url
from django.contrib import admin
#from ajax_select import urls as ajax_select_urls
admin.autodiscover()
# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
#admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'Djembe.views.home', name='home'),
    # url(r'^Djembe/', include('Djembe.foo.urls')),

    url(r'^tracker/',include('tracker.urls')),
    url(r'^search/', include('haystack.urls')),
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
 #   url(r'^admin/lookups/', include(ajax_select_urls)),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$','Djembe.views.index'),
    url(r'^about/','Djembe.views.about'),
    url(r'^music/',include('plugins.music.urls')),
    url(r'^movies/',include('plugins.movies.urls')),
    url(r'^ajax/',include('ajax.urls')),
    url(r'^profile/',include('userprofile.urls')),
    url(r'^user/$','userprofile.views.view'),
    url(r'^users/(?P<username>[\w]+)','userprofile.views.view'),
    url(r'^accounts/',include('invitation.urls')),
    url(r'^accounts/', include('registration.urls')),
    url(r'^forums/',include('forum.urls')),
    url(r'^torrent/',include('torrent.urls')),
    url(r'^static/(?P<path>.*)$', 'django.views.static.serve',
            {'document_root':settings.STATIC_ROOT}),
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root':settings.MEDIA_ROOT}),
)
