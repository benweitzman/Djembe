import bencode
from django.core.urlresolvers import reverse
from django.db.models.aggregates import Sum
from django.forms.util import ErrorList
from django.utils.safestring import mark_safe
import hashlib
from plugins.music.models import *
from tags.models import *
from django.http import  HttpResponse, HttpResponseRedirect, QueryDict
from django.template import RequestContext
from forms import *
from django.shortcuts import render_to_response
from torrent.models import TorrentUploadForm
from photo.forms import PhotoForm

def addArtist(request):
    form = ArtistForm()
    if 'newartist' in request.POST:
        form = ArtistForm(request.POST)
        if form.is_valid():
            artist = form.save()
            return HttpResponseRedirect(reverse(artistPage,kwargs={"artist_id":artist.id}))
    return render_to_response('artists/new.html',context_instance=RequestContext(request,{"form":form}))

def editArtist(request,artist_id):
    artist = Artist.objects.get(id=artist_id)
    form = ArtistForm(instance=artist)
    if request.POST:
        form = ArtistForm(request.POST,instance=artist)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse(artistPage,kwargs={"artist_id":artist.id}))
    return render_to_response('artists/edit.html',context_instance=RequestContext(request,{'form':form}))

def artistsIndex(request):
    if "artist" in request.GET:
        return HttpResponseRedirect(reverse(artistPage,kwargs={"artist_id":request.GET["artist"]}))
    artists = Artist.objects.all()[:5]
    return render_to_response('artists/index.html',{'artists':artists},context_instance=RequestContext(request))

def artistPage(request, artist_id):
    artist = Artist.objects.annotate(
        torrent__count=Count("album__releases__torrents")
    ).annotate(
        snatches=Sum("album__releases__torrents__downloaded")
    ).annotate(
        seeders=Sum("album__releases__torrents__seeders")
    ).annotate(
        leechers=Sum("album__releases__torrents__leechers")
    ).get(id=artist_id)
    albums = dict()
    for release_type in RELEASE_TYPE:
        catAlbums = Album.objects.filter(
            releaseType=release_type[0],
            artists=artist,
        ).order_by("-released")
        albums[release_type[1]] = catAlbums
    return render_to_response('artists/viewArtist.html',context_instance=RequestContext(request,{"artist":artist,
                                                                                                 "albums":albums,}))

def addAlbum(request,artist_id):
    artist = Artist.objects.get(id=artist_id)
    form = AlbumForm(initial={"artists":[artist_id],
                              "name":"Marquee Moon",})
    if request.POST:
        post = request.POST.copy()
        #post.set('artists','b')
        post['artists'] = list(set(map(lambda x:int(x),dict(request.POST)['artists'])))
        form = AlbumForm(post)
        if form.is_valid():
            try:
                a = form.save(commit=True)
                return render_to_response('albums/index.html',context_instance=RequestContext(request,{'album':a,
                                                                                                   'preview':True}))
            except IntegrityError as strerror:
                errors = form._errors.setdefault(forms.forms.NON_FIELD_ERRORS, forms.util.ErrorList())
                errors.append(strerror)

    return render_to_response('albums/new.html',context_instance=RequestContext(request,{"artist":artist,
                                                                                                 "form":form}))

def albumPage(request, album_id):
    album = Album.objects.get(id=album_id)
    photoform = PhotoForm()
    if request.POST:
        photoform = PhotoForm(request.POST)
        if photoform.is_valid():
            photo = photoform.save()
            album.photos.add(photo)
    return render_to_response('albums/index.html',{'album':album,
                                                   'photoForm':photoform},
                                                  context_instance=RequestContext(request))

def addRelease(request,album_id):
    album = Album.objects.get(id=album_id)
    form = ReleaseForm(initial={"album":album})
    if request.POST:
        form = ReleaseForm(request.POST)
        if form.is_valid():
            r = form.save(commit=False)
            r.catalogNumber = r.catalogNumber.rstrip()
            label_name = form.data['label'].rstrip()
            if label_name != "":
                (label,created) = Label.objects.get_or_create(name=label_name)
                r.label = label
            try:
                r.save()
            except IntegrityError as b:
                existing = Release.objects.get(album=r.album,year=r.year,catalogNumber=r.catalogNumber)
                errors = form._errors.setdefault(forms.forms.NON_FIELD_ERRORS, forms.util.ErrorList())
                errors.append("A release already exists with these values:\n%s" % existing)
    return render_to_response('albums/addRelease.html',context_instance=RequestContext(request,{"album":album,
                                                                                                "form":form}))

def addTag(request, album_id):
    if request.POST:
        t = request.POST['tag']
        if not t:
            pass
        album = Album.objects.get(id=album_id)
        if album:
            tag,created = Tag.objects.get_or_create(name=t)
            if album.tagcount_set.filter(tag=tag):
                tagcount = album.tagcount_set.get(tag=tag)
            else:
                tagcount = TagCount.objects.create(album=album,tag=tag)
                tagcount.save()
            album.save()
            tagcount.count = tagcount.count+1
            tagcount.save()
        else:
            print "no album"
        return HttpResponseRedirect(reverse(albumPage,kwargs={"album_id":album.id}))
    return HttpResponseRedirect("/artists/")

def tagVote(request,album_id,tag_id,action):
    album = Album.objects.get(id=album_id)
    tagcount = album.tagcount_set.get(id=tag_id)
    if action == "up":
        tagcount.count += 1
    elif action == "down":
        tagcount.count -= 1
    tagcount.save()
    return HttpResponseRedirect(reverse(albumPage,kwargs={"album_id":album.id}))


def addFormat(request,release_id):
    release = Release.objects.get(id=release_id)
    formatform = FormatForm(initial={"release":release})
    torrentform = TorrentUploadForm(initial={"user":request.user})
    if request.POST:
        formatform = FormatForm(request.POST)
        torrentform = TorrentUploadForm(request.POST,request.FILES)
        if formatform.is_valid() and torrentform.is_valid():
            u = torrentform.save()
            #u.user = request.user
            data = open(u.torrent.file.name,"rb").read()
            torrent = bencode.bdecode(data)
            #u.data = torrent

            #u.info_hash = torrent['info']['']
            s = hashlib.sha1()
            s.update(bencode.bencode(torrent['info']))
            u.info_hash = s.hexdigest()
            exclude = ["pieces"]
            for key in exclude:
                torrent['info'].pop(key,None)
            u.data = torrent['info']
            try:
                u.save()
            except IntegrityError as ie:
                print ie
                print "error"
                print u.torrent
                try:
                    u.torrent.delete()
                except IntegrityError:
                    errors = torrentform._errors.setdefault("torrent", ErrorList())
                    errors.append(u"Duplicate Torrent")
                    u.delete()
                    return render_to_response("release/addFormat.html",context_instance=RequestContext(request,{"release":release,
                                                                                                             "formatform":formatform,
                                                                                                             "torrentform":torrentform}))
                u.delete()
            format = formatform.save(commit=False)
            format.torrent = u
            format.save()
            return HttpResponseRedirect(reverse(albumPage,kwargs={'album_id':release.album.id}))
    return render_to_response('release/addFormat.html',context_instance=RequestContext(request,{"release":release,
                                                                                                "formatform":formatform,
                                                                                                "torrentform":torrentform}))