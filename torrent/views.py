import bencode
import collections
from django.contrib.auth.models import User
from django.utils import simplejson
from userprofile.models import *
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.db.models import Count
from torrent.models import *
from django.forms.util import ErrorList
from django.db import IntegrityError
import hashlib

def get(request, id):
    torrent = Torrent.objects.get(id=id)
    data = open(torrent.torrent.file.name, "rb").read()
    info = bencode.bdecode(data)
    info['announce'] = str("http://localhost:8000/tracker/"+request.user.get_profile().key+"/announce")
    #print info['announce']
    fileName = "file.torrent"
    try:
        fileName = torrent.content_object.fileName()
    except:
        pass
    newTorrent = bencode.bencode(info)
    response = HttpResponse(newTorrent)
    response['Content-Disposition'] = 'attachment; filename='+fileName+".torrent"
    return response

class DivErrorList(ErrorList):
    def __unicode__(self):
        return self.as_divs()
    def as_divs(self):
        if not self: return u''
        return u'<div class="errorlist">%s</div>' % ''.join([u'<div class="alert-message error"><a class="close" href="#">x</a><p><strong>Oh Snap!</strong> %s</p></div>' % e for e in self])

def upload(request):
    if "upload" in request.POST:

        f = TorrentUploadForm(request.POST,request.FILES,error_class=DivErrorList)
        if f.is_valid():
            u = f.save()
            u.user = request.user
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
            except IntegrityError:
                print "error"
                print u.torrent
                try:
                    u.torrent.delete()
                except IntegrityError:
                    errors = f._errors.setdefault("torrent", ErrorList())
                    errors.append(u"Duplicate Torrent")
                    u.delete()
                    return render_to_response("torrent/upload.html",context_instance=RequestContext(request,{"form":f}))
                u.delete()
            return HttpResponseRedirect("/torrent/")

        return render_to_response("torrent/upload.html",context_instance=RequestContext(request,{"form":f}))
    form = TorrentUploadForm()
    return render_to_response("torrent/upload.html",context_instance=RequestContext(request,{"form":form}))

def index(request):
    torrents = Torrent.objects.all()
    return render_to_response("torrent/index.html",context_instance=RequestContext(request,{"torrents":torrents}))
