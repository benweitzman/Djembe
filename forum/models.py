from django.db import models
from django.contrib.auth.models import User

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
        

class Thread(models.Model):
    posts = models.ManyToManyField(Post,null=True,blank=True)
    title = models.CharField(max_length=200)
    op = models.ForeignKey(User)

    def latest_poster(self):
            return self.posts.latest("datePosted").poster

    def latest_post(self):
        return self.posts.latest("datePosted")

class Forum(models.Model):
    threads = models.ManyToManyField(Thread,null=True,blank=True)
    title = models.CharField(max_length=100)
    description = models.TextField(max_length=400)
    category = models.CharField(max_length=25,choices=CATEGORIES)

    def get_latest(self):
        return self.threads.latest("posts__datePosted")
