import bencode
from django.contrib.contenttypes.models import ContentType
from django.core.paginator import Paginator
from django.core.urlresolvers import reverse
from django.db.models import Count
from tags.models import *
from django.db.models.aggregates import Max, Min
from django.forms.formsets import formset_factory
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
    return render_to_response('music/artists/new.html',context_instance=RequestContext(request,{"form":form}))

def editArtist(request,artist_id):
    artist = Artist.objects.get(id=artist_id)
    form = ArtistForm(instance=artist)
    if request.POST:
        form = ArtistForm(request.POST,instance=artist)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse(artistPage,kwargs={"artist_id":artist.id}))
    return render_to_response('music/artists/edit.html',context_instance=RequestContext(request,{'form':form}))

def artistsIndex(request):
    if "artist" in request.GET:
        return HttpResponseRedirect(reverse(artistPage,kwargs={"artist_id":request.GET["artist"]}))
    artists = Artist.objects.annotate(sort=Min("album__releases__torrents__added")).all().order_by('-sort')[:5]
    return render_to_response('music/artists/index.html',{'artists':artists},context_instance=RequestContext(request))

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
    photoform = PhotoForm()
    if request.POST:
        photoform = PhotoForm(request.POST)
        if photoform.is_valid():
            photo = photoform.save()
            artist.photo.add(photo)
    for release_type in RELEASE_TYPE:
        catAlbums = Album.objects.filter(
            releaseType=release_type[0],
            artists=artist,
        ).order_by("-released")
        albums[release_type[1]] = catAlbums
    return render_to_response('music/artists/viewArtist.html',context_instance=RequestContext(request,{"artist":artist,
                                                                                                 "albums":albums,
                                                                                                 "photoForm":photoform}))

def addAlbum(request,artist_id):
    artist = Artist.objects.get(id=artist_id)
    form = AlbumForm(initial={"artists":[artist_id]})
    artistFormSet= formset_factory(ArtistNameForm,extra=0,formset=BaseArtistNameFormSet)
    artistsWithName = Artist.objects.filter(name=artist.name)
    artists = artistFormSet(initial=[
        {"name":artist.name,"choices":map(lambda x:(x.id,x.id),artistsWithName),"id":artist_id}
    ])
    if request.POST:
        post = request.POST.copy()
        #post.set('artists','b')
        #post['artists'] = list(set(map(lambda x:int(x),dict(request.POST)['artists'])))
        form = AlbumForm(post)
        artists = artistFormSet(request.POST)#,initial=[{"choices":map(lambda x:(x.id,x.id),artistsWithName)}])
        for aform in artists:
            nameArtists = Artist.objects.filter(name=aform['name'].value())
            aform.fields['id'].choices = map(lambda x:(x.id,x.id),nameArtists)
            if len(nameArtists) == 1:
                aform.fields['id'].widget.attrs['style'] = "display:none"
        if artists.is_valid() and form.is_valid():
            try:
                a = form.save()
                print artists.cleaned_data
                for artist in artists.cleaned_data:
                    if artist['id'] == u'' or artist['id'] == None:
                        newArtist = Artist.objects.create(name=artist['name'])
                    else:
                        newArtist = Artist.objects.get(id=int(artist['id']))
                    a.artists.add(newArtist)
                a.save()
                return render_to_response('music/albums/viewAlbum.html',context_instance=RequestContext(request,{'album':a,
                                                                                                   'preview':True}))
            except IntegrityError as strerror:
                errors = form._errors.setdefault(forms.forms.NON_FIELD_ERRORS, forms.util.ErrorList())
                errors.append(strerror)

    return render_to_response('music/albums/new.html',context_instance=RequestContext(request,{"artist":artist,
                                                                                         "form":form,
                                                                                         "artists":artists}))
def albumsIndex(request):
    albums = Album.objects.annotate(sort=Min("releases__torrents__added")).order_by('-sort')[:5]
    return render_to_response('music/albums/index.html',context_instance=RequestContext(request,{"albums":albums}))


def albumPage(request, album_id):
    album = Album.objects.get(id=album_id)
    photoform = PhotoForm()
    if request.POST:
        if "photoform" in request.POST:
            photoform = PhotoForm(request.POST)
            if photoform.is_valid():
                photo = photoform.save()
                album.photos.add(photo)
        elif "commentform" in request.POST:
            comment = request.POST['body']
            index = album.comments.count()
            post = Post.objects.create(text=comment,poster=request.user,index=index)
            album.comments.add(post)
            album.save()
    page = request.GET['page'] if request.GET.get('page') else 1
    if request.GET.get('post'):
        post = album.comments.get(id=request.GET.get('post'))
        page = post.index/10+1
    p = Paginator(album.comments.all(),10)
    showpages = 9
    startpage = 0
    stoppage = p.num_pages
    if stoppage>showpages:
        startpage=int(page)-round(showpages/2)-1
        if startpage <= 0:
            startpage = 0
        elif startpage >= p.num_pages-showpages:
            startpage = p.num_pages-showpages
        stoppage=startpage+showpages
    pages = map(lambda x: p.page(x),p.page_range)
    showPages = dict(enumerate(pages[int(startpage):int(stoppage)]))
    posts = p.page(page)
    return render_to_response('music/albums/viewAlbum.html',{"album":album,
                                                       "photoForm":photoform,
                                                       "pages":pages,
                                                       "posts":posts,
                                                       "showPages":showPages,
                                                       "startPage":startpage,
                                                       "stopPage":stoppage},
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
    return render_to_response('music/albums/addRelease.html',context_instance=RequestContext(request,{"album":album,
                                                                                                "form":form}))

def addTag(request, album_id):
    if request.POST:
        t = request.POST['tag']
        if not t:
            pass
        album = Album.objects.get(id=album_id)
        if album:
            tag,created = Tag.objects.get_or_create(name=t)
            if album.tags.filter(tag=tag):
                tagcount = album.tags.get(tag=tag)
            else:
                tagcount = TagCount.objects.create(tag=tag)
                tagcount.save()
            album.tags.add(tagcount)
            album.save()
            tagcount.save()
        else:
            print "no album"
        return HttpResponseRedirect(reverse(albumPage,kwargs={"album_id":album.id}))
    return HttpResponseRedirect("/artists/")

def tagVote(request,album_id,tag_id,action):
    album = Album.objects.get(id=album_id)
    tagcount = TagCount.objects.get(id=tag_id)
    vote,created = TagVote.objects.get_or_create(user=request.user,tag=tagcount)
    if action == "up":
        vote.way = 1
    elif action == "down":
        vote.way = -1
    vote.save()
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
            u.content_type = ContentType.objects.get(model='albumformat')
            u.object_id = format.id
            u.save()
            return HttpResponseRedirect(reverse(albumPage,kwargs={'album_id':release.album.id}))
    return render_to_response('music/release/addFormat.html',context_instance=RequestContext(request,{"release":release,
                                                                                                "formatform":formatform,
                                                                                                "torrentform":torrentform}))
