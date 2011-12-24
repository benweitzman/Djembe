from groups.models import *
from tags.models import *
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response

def artistsIndex(request):
    if "artist" in request.GET:
        return HttpResponseRedirect("/artists/"+request.GET["artist"])
    artists = Artist.objects.all()[:5]
    return render_to_response('artists/index.html',{'artists':artists},context_instance=RequestContext(request))

def artistPage(request, artist_name):
    artist = Artist.objects.get(name=artist_name)
    albums = dict()
    for release_type in RELEASE_TYPE:
        catAlbums = Album.objects.filter(
            releaseType=release_type[0],
            artists=artist,
        )
        albums[release_type[1]] = catAlbums
    return render_to_response('artists/viewArtist.html',context_instance=RequestContext(request,{"artist":artist,
                                                                                                 "albums":albums,}))

def albumPage(request, album_name):
    album = Album.objects.get(name=album_name)
    return render_to_response('albums/index.html',{'album':album},
                                                  context_instance=RequestContext(request))

def addTag(request, album_name):
    if request.POST:
        t = request.POST['tag']
        album = Album.objects.get(name=album_name)
        if album:
            tags = Tag.objects.filter(name=t)
            if tags:
                itag = tags[0]
                if album.tagcount_set.filter(tag=itag):
                    tagcount = album.tagcount_set.get(tag=itag)
                else:
                    tagcount = TagCount.objects.create(album=album,tag=itag)
                    tagcount.save()
                #album.tags.add(tag)
            else:
                tag = Tag.objects.create(name=t)
                tagcount = TagCount.objects.create(album=album,tag=tag)
                tag.save()
                tagcount.save()
                #album.tags.add(tag)
            album.save()
            tagcount.count = tagcount.count+1
            tagcount.save()
        else:
            print "no album"
        return HttpResponseRedirect("/albums/"+album.name)
    return HttpResponseRedirect("/artists/")

