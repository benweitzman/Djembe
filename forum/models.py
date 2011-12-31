from Dialog import Event
from django.core.urlresolvers import reverse
from django.db import models
from django.contrib.auth.models import User
from django.db.models import Count

CATEGORIES = (
    ("site","Site"),
    ("community","Community"),
)

class Post(models.Model):
    poster = models.ForeignKey(User)
    text = models.TextField()
    datePosted = models.DateTimeField(auto_now_add=True)
    dateModified = models.DateTimeField(auto_now=True)
    editor = models.ForeignKey(User,related_name="editor",null=True,blank=True)
    index = models.IntegerField()
        

class Thread(models.Model):
    posts = models.ManyToManyField(Post,null=True,blank=True)
    title = models.CharField(max_length=200)
    op = models.ForeignKey(User)

    @models.permalink
    def get_absolute_url(self):
        return ('forum.views.viewThread',[str(self.id)])

    def latest_poster(self):
            return self.posts.latest("datePosted").poster

    def latest_post(self):
        return self.posts.latest("datePosted")

    def __unicode__(self):
        return self.title

class Forum(models.Model):
    threads = models.ManyToManyField(Thread,null=True,blank=True)
    title = models.CharField(max_length=100)
    description = models.TextField(max_length=400)
    category = models.CharField(max_length=25,choices=CATEGORIES)

    def get_latest(self):
        try:
            return Thread.objects.annotate(Count("posts")).get(id=self.threads.latest("posts__datePosted").id)
        except Thread.DoesNotExist:
            return

    def __unicode__(self):
        return self.title
