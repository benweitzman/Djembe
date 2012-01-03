from django.conf.urls.defaults import *

urlpatterns = patterns('plugins.music.views',
    url(r'^artists/$', 'artistsIndex'),
    url(r'^artists/new/$','addArtist'),
    url(r'^artists/(?P<artist_id>\d+)/$', 'artistPage'),
    url(r'^artists/(?P<artist_id>\d+)/edit/$', 'editArtist'),
    url(r'^artists/(?P<artist_id>\d+)/new/$', 'addAlbum'),
    url(r'^albums/$','albumsIndex'),
    url(r'^albums/(?P<album_id>\d+)/$', 'albumPage'),
    url(r'^albums/(?P<album_id>\d+)/addtag/$', 'addTag'),
    url(r'^albums/(?P<album_id>\d+)/(?P<tag_id>\d+)/(?P<action>\w+)','tagVote'),
    url(r'^albums/(?P<album_id>\d+)/add/$','addRelease'),
    url(r'^releases/(?P<release_id>\d+)/add/$','addFormat'),
)