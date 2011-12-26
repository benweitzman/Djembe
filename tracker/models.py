from django.contrib.auth.models import User
from torrent.models import Torrent
from userprofile.models import UserProfile
from django.db import models

class Peer(models.Model):
    user = models.ForeignKey(User, null=True, related_name='connections')
    torrent = models.ForeignKey(Torrent, related_name='peers')
    peer_id = models.CharField( max_length=128, db_index=True)
    ip = models.GenericIPAddressField(default='127.0.0.1')
    port = models.PositiveIntegerField(default=0)
    key = models.CharField(max_length=255, default='')
    uploaded = models.PositiveIntegerField(default=0)
    downloaded = models.PositiveIntegerField(default=0)
    left = models.PositiveIntegerField(default=0)
    timestamp = models.DateTimeField(auto_now=True)
