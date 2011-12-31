from haystack.indexes import *
from haystack import site
from plugins.music.models import *

class AlbumIndex(SearchIndex):
    text = CharField(document=True,use_template=True)
    name = CharField(model_attr='name')
    #artist = MultiValueField(model_attr='artists')

    def index_queryset(self):
        return Album.objects.all()

class ArtistIndex(SearchIndex):
    text = CharField(document=True,use_template=True)
    name = CharField(model_attr='name')

    def index_queryset(self):
        return Artist.objects.all()


site.register(Artist, ArtistIndex)
site.register(Album, AlbumIndex)