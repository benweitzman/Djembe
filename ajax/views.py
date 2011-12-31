from django.http import HttpResponse
from django.utils import simplejson
from plugins.music.models import *
from forum.models import *
from django.contrib.auth.models import User

def checkUnique(request):
    message = False
    if request.is_ajax or True:
        kind = request.GET['kind']
        letters = request.GET['letters']
        if kind == "artists":
            if Artist.objects.filter(name=letters):
                message = True
    return HttpResponse(simplejson.dumps(message))

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
            a = User.objects.extra(select={"name":"username"}).values('name').filter(username__startswith=letters)
            if a:
                response['users'] = list(a)
        if kind == "forums" or 4 in searchtypes:
            a = Thread.objects.extra(select={"name":"title"}).values('name').filter(title__startswith=letters)
            if a:
                response['forums'] = list(a)
        if len(response) != 0:
            message = simplejson.dumps(response)
    return HttpResponse(message)

#def mega(request):
    #if request.is_ajax():
        
