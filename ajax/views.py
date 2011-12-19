from django.http import HttpResponse
from django.utils import simplejson
from groups.models import *
from django.contrib.auth.models import User

def index(request):
    message= "[]"
    if request.is_ajax() or True:
        kind = request.GET['kind']
        letters = request.GET['letters']
        model = Artist
        response = dict()
        searchtypes = list()
        if kind == "mega":
            searchtypes = request.user.get_profile().searchtypes()
        if kind == "artists" or 1 in searchtypes:
            a = Artist.objects.values('name').filter(name__startswith=letters)
            if a:
                response['artists'] = list(a)
        if kind == "albums" or 2 in searchtypes:
            a = Album.objects.filter(name__startswith=letters)
            albumArtists = list()
            for album in a:
                newAlbum = dict()
                newAlbum['name'] = album.name
                newAlbum['artists'] = list(album.artists.all().values('name'))
                albumArtists.append(newAlbum)
            if albumArtists:
                response['albums'] = albumArtists
        if kind == "users" or 3 in searchtypes:
            a = User.objects.values('username').filter(username__startswith=letters)
            if a:
                response['users'] = list(a)
        if len(response) != 0:
            message = simplejson.dumps(response)
    return HttpResponse(message)

#def mega(request):
    #if request.is_ajax():
        
