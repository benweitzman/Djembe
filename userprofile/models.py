from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.forms import ModelForm
from django import forms

SEARCH_TYPES = (
    (1,"Artists"),
    (2,"Albums"),
    (3,"Users"),
)

class UserProfile(models.Model):
    user = models.OneToOneField(User)
    avatar = models.CharField(max_length=400)
    profile = models.TextField(blank=True,null=True)
    megasearch = models.CharField(max_length=20)

    def searchtypes(self):
        strings = self.megasearch.split(",")
        nums = list()
        for i in strings[:-1]:
            nums.append(int(i))
        return nums

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