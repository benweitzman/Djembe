from groups.models import *
from tags.models import *
from django.http import HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response

def index(request):
    artists = Artist.objects.all()[:5]
    return render_to_response('artists/index.html',{'artists':artists})

def artistPage(request, artist_name):
    return HttpResponse("Artist: %s" % artist_name)

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
                tagcount.count = tagcount.count+1
                tagcount.save()
                #album.tags.add(tag)
            else:
                tag = Tag.objects.create(name=t)
                album.tags.add(tag)
            album.save()
        else:
            print "no album"
    return HttpResponse("hi!")