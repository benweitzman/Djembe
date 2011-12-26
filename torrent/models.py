from annoying.fields import JSONField
from django.db import models
from django.contrib.auth.models import User
from django.forms import ModelForm
from django import forms
#from django.db.models.fields import SlugField

class Torrent(models.Model):
    title = models.CharField(max_length=80)
    #slug = SlugField()
    user = models.ForeignKey(User, blank=True, null=True, verbose_name='Author')
    #image = models.ImageField(_('Image'), upload_to='img/torrents', blank=True, null=True)
    description = models.TextField()
    added = models.DateTimeField(auto_now_add=True, editable=False)
    torrent = models.FileField(upload_to='torrent/')
    data = JSONField(editable=False, default=lambda: {})
    info_hash = models.CharField(unique=True, max_length=40, db_index=True, editable=False)
    seeders = models.PositiveIntegerField(editable=False, default=0)
    leechers = models.PositiveIntegerField(editable=False, default=0)
    downloaded = models.PositiveIntegerField(editable=False, default=0)

class TorrentUploadForm(ModelForm):
    class Meta:
        model = Torrent
        exclude = ("user")