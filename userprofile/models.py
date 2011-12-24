from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.forms import ModelForm
from django import forms
from forum.models import *

SEARCH_TYPES = (
    (1,"Artists"),
    (2,"Albums"),
    (3,"Users"),
)

PPP = (
    (25,25),
    (50,50),
    (100,100),
)

class ThreadView(models.Model):
    user = models.ForeignKey(User)
    thread = models.ForeignKey(Thread)
    post = models.ForeignKey(Post)

    class Meta:
        unique_together = ('user','thread')

    def __unicode__(self):
        return self.user.username+u':'+self.thread.title+u':'+str(self.post.id)

class UserProfile(models.Model):
    user = models.OneToOneField(User)
    avatar = models.CharField(max_length=400)
    profile = models.TextField(blank=True,null=True)
    postsPerPage = models.IntegerField(default=25,)
    megasearch = models.CharField(max_length=20)

    def searchtypes(self):
        strings = self.megasearch.split(",")
        nums = list()
        for i in strings[:-1]:
            nums.append(int(i))
        return nums

    def __unicode__(self):
        return self.user.username

class ProfileForm(ModelForm):
    class Meta:
        model = UserProfile
        exclude = ("user")
    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)
        self.fields['megasearch'] = forms.MultipleChoiceField(choices=SEARCH_TYPES)
        self.fields['megasearch'].widget = forms.CheckboxSelectMultiple(choices=SEARCH_TYPES)

def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

post_save.connect(create_user_profile, sender=User)