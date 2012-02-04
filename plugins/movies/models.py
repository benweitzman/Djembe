from django.db import models
from django.contrib.auth.models import User
from forum.models import Post
from photo.models import Photo
from tags.models import TagCount
from torrent.models import Torrent

CODECS = (
    ("XviD","XviD"),
    ("DivX","DivX"),
    ("H.264","H.264"),
    ("x264","x264"),
)

CONTAINERS = (
    ("AVI","AVI"),
    ("MPG","MPG"),
    ("MKV","MKV"),
    ("MP4","MP4"),
)

RESOLUTIONS = (
    ("480p","480p"),
    ("576p","576p"),
    ("720p","720p"),
    ("1080p","1080p"),
    ("1080i","1080i"),
)

MEDIAS = (
    ("DVD","DVD"),
    ("Blu-ray","Blu-ray"),
    ("HDTV","HDTV"),
    ("HD-DVD","HD-DVD"),
    ("TV","TV")
)

class Person(models.Model):
    name = models.CharField(max_length=200)

    #@models.permalink
    #def get_absolute_url(self):
    #    return ('plugins.movies.views.')

    def __unicode__(self):
        return self.name

class Actor(models.Model):
    person = models.ForeignKey(Person)
    movie = models.ForeignKey('Movie')
    role = models.CharField(max_length=200)

class Movie(models.Model):
    photos = models.ManyToManyField(Photo,blank=True)
    tags = models.ManyToManyField(TagCount)
    comments = models.ManyToManyField(Post,editable=False)
    title = models.CharField(max_length=200)
    year = models.IntegerField('Year Released')
    directors = models.ManyToManyField(Person,related_name='directed')
    writers = models.ManyToManyField(Person,related_name='written',blank=True)
    producers = models.ManyToManyField(Person,related_name='produced',blank=True)
    actors = models.ManyToManyField(Person,through=Actor,related_name='actedIn',blank=True)

    @models.permalink
    def get_absolute_url(self):
        return ('plugins.movies.views.filmPage',[str(self.id)])

    def save(self,*args,**kwargs):
        super(Movie,self).save(*args,**kwargs)
        if not self.editions.all():
            original = Edition.objects.create(year=self.year,name="Original Release",movie=self)
            
    def __unicode__(self):
        return self.title

class Edition(models.Model):
    movie = models.ForeignKey(Movie,related_name='editions')
    name = models.CharField(max_length=200)
    year = models.IntegerField(blank=True,null=True)
    torrents = models.ManyToManyField(Torrent,through='MovieFormat',blank=True)

class MovieFormat(models.Model):
    torrent = models.ForeignKey(Torrent)
    edition = models.ForeignKey(Edition)
    codec = models.CharField(max_length=10,choices=CODECS)
    container = models.CharField(max_length=10,choices=CONTAINERS)
    resolution = models.CharField(max_length=10,choices=RESOLUTIONS)
    source = models.CharField(max_length=10,choices=MEDIAS)
    

