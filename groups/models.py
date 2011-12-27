from django.db import models
from tags.models import Tag
from photo.models import Photo
import torrent
from torrent.models import Torrent

RELEASE_TYPE = (
    ("album","Album"),
    ("ep","EP"),
    ("single","Single"),
    ("compilation","Compilation"),
    ("anthology","Anthology"),
)

FORMATS = (
    ("mp3","MP3"),
    ("flac","FLAC"),
)

BITRATES = (
    ("320","320"),
    ("lossless","Lossless"),
)

MEDIAS = (
    ("cd","CD"),
)

class Album(models.Model):
    artists = models.ManyToManyField('Artist')
    #releases = models.ManyToManyField('Release',blank=True,related_name='album')
    name = models.CharField(max_length=100)
    released = models.IntegerField('Year released')
    tags = models.ManyToManyField(Tag,blank=True, through='TagCount')
    photos = models.ManyToManyField(Photo,blank=True)
    releaseType = models.CharField(max_length=15,choices=RELEASE_TYPE,default="album")
    albumInfo = models.TextField(blank=True,null=True)

    def save(self,*args,**kwargs):
        super(Album,self).save(*args,**kwargs)
        if not self.releases.all():
            original = Release.objects.create(year=self.released,title="Original Release",album=self)
            original.save()

    def __unicode__(self):
        return self.name

class Artist(models.Model):
    name = models.CharField(max_length=100)
    artistInfo = models.TextField(blank=True,null=True)
    photo = models.ManyToManyField(Photo,blank=True)

    def __unicode__(self):
        return self.name


class Label(models.Model):
    name = models.CharField(max_length=100)

    def __unicode__(self):
        return self.name

class Release(models.Model):
    album = models.ForeignKey(Album,related_name="releases")
    label = models.ForeignKey(Label, null=True,blank=True)
    catalogNumber = models.CharField(max_length=100,blank=True)
    year = models.IntegerField()
    title = models.CharField(max_length=100,blank=True)
    torrents = models.ManyToManyField(Torrent,through='AlbumFormat',blank=True,null=True)

    def format(self):
        formatted = str(self.year)
        if self.title:
            formatted += " / "+self.title
        if self.label:
            formatted += " / "+str(self.label)
        if self.catalogNumber:
            if not self.label:
                formatted += " / "
            else:
                formatted += " "
            formatted += self.catalogNumber
        return formatted

    def __unicode__(self):
        return self.album.name+": "+self.format()

class AlbumFormat(models.Model):
    release = models.ForeignKey('Release')
    torrent = models.ForeignKey(Torrent)
    format = models.CharField(max_length=5,choices=FORMATS)
    bitrate = models.CharField(max_length=10,choices=BITRATES)
    media = models.CharField(max_length=2,choices=MEDIAS)

    def fileName(self):
        return self.release.album.name+" ("+str(self.release.album.released)+") ["+self.format.upper()+"]"


class TagCount(models.Model):
    album = models.ForeignKey(Album)
    tag = models.ForeignKey(Tag, related_name="tag_name")
    count = models.IntegerField(default=0)

    def __unicode__(self):
        return self.album.name+":"+self.tag.name
