from urlparse import parse_qsl
from bencode import *
from django.contrib.auth.models import User
from django.utils import simplejson
from django.utils.datastructures import MultiValueDictKeyError
from tracker.models import Peer
from userprofile.models import *
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.db.models import Count
from userprofile.models import UserProfile
from torrent.models import *
from django.forms.util import ErrorList
from django.db import IntegrityError


def announce(request,key):
    #raise Http404
    print 'blah'
    query = dict(parse_qsl(request.META['QUERY_STRING']))
    if not query.get('info_hash'):
        raise Http404
    info_hash = query['info_hash'].encode('hex')

    response = {'interval': 60}
    try:
        print 'hmm'
        try:
            torrent = Torrent.objects.get(info_hash=info_hash)
        except :
            raise Torrent.DoesNotExist()
        # required fields
        ip = request.META['REMOTE_ADDR']
        port = request.GET['port']
        peer_id = request.GET['peer_id']
        event = request.GET.get('event')
        numwant = request.GET.get('numwant',50)
        #print str(unicode(peer_id))
        # tracking fields
        uploaded = int(request.GET['uploaded'])
        downloaded = int(request.GET['downloaded'])
        left = int(request.GET['left'])
        compact = request.GET.get('compact', 0)

        # keying for keeping the trash out. DIE UNWASHED MASSES, DIE.
        if key:
            try:
                profile = UserProfile.objects.get(key = key)
            except UserProfile.DoesNotExist:
                raise ValueError('you are not allowed on this tracker')

        # SPEED UP WITH REDIS
        print 'ifelse'
        if event:
            if 'started' in event:
                print 'started'
                peer, created = Peer.objects.get_or_create(peer_id=peer_id,torrent=torrent,ip=ip,port=port)
                print created
                if created:
                    #if key and 'profile' in locals():
                    peer.user = profile.user
                    peer.ip = ip
                    peer.port = port
                    peer.save()
                    torrent.seeders += 1
                    if torrent.downloaded == 0 and left == 0:
                        torrent.downloaded += 1
                    torrent.save()
            elif 'stopped' in event:
                try:
                    print 'stopped'
                    peer = Peer.objects.get(peer_id=peer_id, torrent=torrent)
                    print peer
                    peer.delete()
                    print 'deleted'
                    torrent.seeders -= 1
                    torrent.save()
                except Peer.DoesNotExist:
                    pass
                return
            elif 'completed' in event:
                print 'completeed'
                torrent.downloaded += 1
                torrent.save()
                try:
                    peer = Peer.objects.get(peer_id=peer_id, torrent=torrent)
                    user = peer.user
                    profile = user.get_profile()
                    profile.snatched.add(torrent)
                    profile.save()
                except Peer.DoesNotExist:
                    pass
        else:
            try:
                peer = Peer.objects.get(peer_id=peer_id,torrent=torrent)
            except Peer.DoesNotExist:
                pass
        print "guvnah"
        ddiff = downloaded-peer.downloaded
        profile.downloaded += ddiff
        udiff = uploaded-peer.uploaded
        profile.uploaded += udiff
        peer.downloaded=downloaded
        peer.uploaded=uploaded
        peer.save()
        profile.save()
        def removeNonAscii(s): return "".join(i for i in s if ord(i)<128)

        if numwant:
                # The random order is expensive. by caching for the announce interval, we guarantee that
                # a random peer list will be generated every announce period and will be served to all clients
                # looking for that info. The expiry guarantees that new results will be generated on next announce
            peers = [dict((pkey.replace('_', ' '), str(value)) for pkey, value in peer.iteritems())
                 for peer in torrent.peers.order_by('?').values('port','ip')[:100] ]
            print peers
                #cache.set("tracker-peers-iphandout-"+info_hash, peers, settings.TRACKER_ANNOUNCE_INTERVAL)
            response['peers'] = peers[:min(numwant, 100)]
        print 'finished'
    except MultiValueDictKeyError:
        response['failure reason'] = 'invalid request, duplicate GET keys.'
    except Torrent.DoesNotExist:
        response['failure reason'] = 'torrent not available'
    except ValueError, e:
        response['failure reason'] = str(e)
    finally:
        if response.get('failure reason'): response['interval']=20
        return HttpResponse(bencode(response), content_type='text/plain')

