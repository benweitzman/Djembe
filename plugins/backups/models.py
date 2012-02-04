from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.contrib.auth.models import User
from django.db.models.aggregates import Sum
from torrent.models import Torrent
from tracker.models import Peer

class BackupUser(models.Model):
    user = models.ForeignKey(User,unique=True)
    uploaded = models.IntegerField(default=0)
    downloaded = models.IntegerField(default=0)
    priorityPoints = models.IntegerField(default=0)
    snatched = models.ManyToManyField("Version",blank=True)
    subscribed = models.ManyToManyField("Backup",blank=True)

    def get_downloaded(self):
        contentType = ContentType.objects.get(model='version')
        peers = Peer.objects.filter(user=self.user,torrent__content_type=contentType)
        return peers.aggregate(Sum('downloaded'))

    def get_uploaded(self):
        versions = Version.objects.filter(backup__owner=self.user)
        torrents = map(lambda x:x.torrent,versions)
        peers = Peer.objects.filter(torrent__in=torrents,user__not=self.user)
        return peers.aggregate(Sum('downloaded'))

class Backup(models.Model):
    owner = models.ForeignKey(User,editable=False)
    name = models.CharField(max_length=200)
    redundancy = models.IntegerField()
    priorityPoints = models.IntegerField()

class Version(models.Model):
    torrent = models.ForeignKey(Torrent)
    number = models.IntegerField(blank=True,null=True)
    backup = models.ForeignKey(Backup)
    date = models.DateTimeField(auto_now_add=True)
    message = models.TextField(blank=True,null=True)
