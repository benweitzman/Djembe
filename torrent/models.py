from annoying.fields import JSONField
from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.contrib.auth.models import User
from django.forms import ModelForm
from django import forms
#from django.db.models.fields import SlugField

class Torrent(models.Model):
    #slug = SlugField()
    user = models.ForeignKey(User, blank=True, null=True, verbose_name='Author')
    #image = models.ImageField(_('Image'), upload_to='img/torrents', blank=True, null=True)
    description = models.TextField(blank=True,null=True)
    added = models.DateTimeField(auto_now_add=True, editable=False)
    torrent = models.FileField(upload_to='torrent/',max_length=200)
    data = JSONField(editable=False, default=lambda: {})
    info_hash = models.CharField(unique=True, max_length=40, db_index=True, editable=False)
    seeders = models.PositiveIntegerField(editable=False, default=0)
    leechers = models.PositiveIntegerField(editable=False, default=0)
    downloaded = models.PositiveIntegerField(editable=False, default=0)

    content_type = models.ForeignKey(ContentType,editable=False)
    object_id = models.PositiveIntegerField(editable=False)
    content_object = generic.GenericForeignKey('content_type', 'object_id')

    def getSeeders(self):
        return self.peers.filter(left=0).count()
    
    def getLeechers(self):
        return self.peers.exclude(left=0).count()
        
    def size(self):
        if 'length' in self.data:
            return self.data['length']
        else:
            length = 0
            for i in self.data['files']:
                length += i['length']
            return length

class TorrentUploadForm(ModelForm):
    class Meta:
        model = Torrent
        widgets = (
            {"user":forms.HiddenInput()}
        )