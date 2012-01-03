from django.db import models
from django.db.models import Sum
from django.contrib.auth.models import User
from django.db.utils import IntegrityError
from forum.models import Post
from tags.models import Tag
from photo.models import Photo
from django.db.models.signals import m2m_changed
from django.dispatch import receiver

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

VOTES = (
    (-1,"down"),
    (1,"up"),
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
    comments = models.ManyToManyField(Post)

    @models.permalink
    def get_absolute_url(self):
        return ('plugins.music.views.albumPage',[str(self.id)])

    def save(self,*args,**kwargs):
        super(Album,self).save(*args,**kwargs)
        if not self.releases.all():
            original = Release.objects.create(year=self.released,title="Original Release",album=self)
            original.save()

    def __unicode__(self):
        return self.name

@receiver(m2m_changed, sender=Album.artists.through)
def verify_uniqueness(sender, **kwargs):
    album = kwargs.get('instance', None)
    action = kwargs.get('action', None)
    artists = kwargs.get('pk_set', None)

    if action == 'pre_add':
        for artist in artists:
            if Album.objects.filter(name=album.name).filter(artists=artist):
                raise IntegrityError('Album with name %s already exists for artist %s' % (album.name, Artist.objects.get(pk=artist)))


class Artist(models.Model):
    name = models.CharField(max_length=100)
    artistInfo = models.TextField(blank=True,null=True,verbose_name='Artist Info')
    photo = models.ManyToManyField(Photo,blank=True)

    def taglist(self):
        tags = dict()
        for album in self.album_set.all():
            album_tags = album.tags.all()
            for tag in album_tags:
                if tag.name in tags:
                    tags[tag.name] += 1
                else:
                    tags[tag.name] = 1
        tags = tags.items()
        tags.sort(key=lambda tup:tup[1],reverse=True)
        return tags

    def __unicode__(self):
        return self.name

    @models.permalink
    def get_absolute_url(self):
        return ('plugins.music.views.artistPage',[str(self.id)])



class Label(models.Model):
    name = models.CharField(max_length=100,unique=True)

    def __unicode__(self):
        return self.name

class Release(models.Model):
    album = models.ForeignKey(Album,related_name="releases")
    label = models.ForeignKey(Label, null=True,blank=True)
    catalogNumber = models.CharField(max_length=100,blank=True,verbose_name="Catalog Number")
    year = models.IntegerField()
    title = models.CharField(max_length=100,blank=True)
    torrents = models.ManyToManyField(Torrent,through='AlbumFormat',blank=True,null=True)
    class Meta:
        unique_together = ('album','label','year','catalogNumber')
        unique_together = ('album','year','catalogNumber')

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



class TagVotes(models.Model):
    tag = models.ForeignKey('TagCount')
    user = models.ForeignKey(User)
    way = models.IntegerField(choices=VOTES,default=1)

class TagCount(models.Model):
    album = models.ForeignKey(Album)
    tag = models.ForeignKey(Tag, related_name="tag_name")
    count = models.IntegerField(default=0)
    voters = models.ManyToManyField(User,through=TagVotes)

    class Meta:
        ordering = ['-count','tag']

    def __unicode__(self):
        return self.album.name+":"+self.tag.name

    def save(self, *args, **kwargs):
        self.count = self.getCount()
        super(TagCount,self).save(*args,**kwargs)

    def getCount(self):
        count = 15
        votes = self.tagvotes_set.aggregate(count=Sum('way'))['count']
        if votes: count += votes
        return count
