from django.db import models
from tags.models import Tag
from photo.models import Photo

RELEASE_TYPE = (
    ("album","Album"),
    ("ep","EP"),
    ("single","Single"),
    ("compilation","Compilation"),
    ("anthology","Anthology"),
)

class Album(models.Model):
    artists = models.ManyToManyField('Artist')
    releases = models.ManyToManyField('Release',blank=True)
    name = models.CharField(max_length=100)
    released = models.DateField('Date released')
    tags = models.ManyToManyField(Tag,blank=True, through='TagCount')
    photo = models.ManyToManyField(Photo,blank=True)
    releaseType = models.CharField(max_length=15,choices=RELEASE_TYPE,default="album")
    def __unicode__(self):
        return self.name

class Artist(models.Model):
    name = models.CharField(max_length=100)
    #albums = models.ManyToManyField('Album',blank=True,db_table="groups_album_artists")
    photo = models.ManyToManyField(Photo,blank=True)

    def __unicode__(self):
        return self.name


class Label(models.Model):
    name = models.CharField(max_length=100)

    def __unicode__(self):
        return self.name

class Release(models.Model):
    related_album = models.ForeignKey(Album)
    label = models.ForeignKey(Label, null=True,blank=True)
    catalogNumber = models.CharField(max_length=100,blank=True)
    year = models.IntegerField()
    title = models.CharField(max_length=100,blank=True)

    def __unicode__(self):
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

class TagCount(models.Model):
    album = models.ForeignKey(Album)
    tag = models.ForeignKey(Tag, related_name="tag_name")
    count = models.IntegerField(default=0)

    def __unicode__(self):
        return self.album.name+":"+self.tag.name
