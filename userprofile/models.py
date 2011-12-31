import random
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.forms import ModelForm
from django import forms
from django.utils.safestring import mark_safe
from forum.models import *
from torrent.models import Torrent

SEARCH_TYPES = (
    (1,"Artists"),
    (2,"Albums"),
    (3,"Users"),
    (4,"Forums"),
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

class MyCheckboxSelectMultiple(forms.CheckboxSelectMultiple):
    def render(self, name, value, attrs=None, choices=()):
        html = super(MyCheckboxSelectMultiple, self).render(name, value, attrs, choices)

        return mark_safe(html.replace('<ul>', '<ul class="inputs-list">'))

class UserProfile(models.Model):
    user = models.OneToOneField(User)
    avatar = models.CharField(max_length=400,blank=True)
    profile = models.TextField(blank=True,null=True)
    postsPerPage = models.IntegerField(default=25,choices=PPP,verbose_name="Posts Per Page")
    megasearch = models.CharField(max_length=200,blank=True)
    key = models.CharField(max_length=35,editable=False,default='')
    invites = models.IntegerField(editable=False,default=0)# -1 = inf
    snatched = models.ManyToManyField(Torrent)

    class Meta:
        permissions = (
            ("can_invite","Can send invites"),
        )

    def searchtypes(self):
        strings = self.megasearch.split(",")
        nums = list()
        for i in strings[:-1]:
            nums.append(int(i))
        return nums

    def save(self, *args, **kwargs):
        if self.key == '':
            self.key = ''.join(random.choice('0987654321poiuytrewqlkjhgfdsmnbvcxz') for i in range(35))
        super(UserProfile,self).save(*args,**kwargs)

    def __unicode__(self):
        return self.user.username

class ProfileForm(ModelForm):
    class Meta:
        model = UserProfile
        exclude = ("user")
    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)
        self.fields['avatar'].widget.attrs = {"class":"xxlarge"}
        self.fields['profile'].widget.attrs = {"class":"xxlarge","style":"height:100px !important"}
        self.fields['megasearch'] = forms.MultipleChoiceField(choices=SEARCH_TYPES)
        self.fields['megasearch'].widget = MyCheckboxSelectMultiple(choices=SEARCH_TYPES)

def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

post_save.connect(create_user_profile, sender=User)