from itertools import chain
from optparse import _
from django import forms
from django.core.exceptions import ValidationError
from django.db.models.fields import TextField
from django.forms import ModelForm
from django.forms.widgets import Widget
from django.forms.util import flatatt
from django.forms.widgets import TextInput
from django.utils import simplejson
from django.utils.encoding import force_unicode, smart_unicode
from django.utils.safestring import mark_safe
from django.utils.html import escape, conditional_escape
from django.utils.translation import ugettext_lazy as _
from django.core.validators import EMPTY_VALUES
from django.contrib.auth.models import User
from taggit.forms import TagField

from models import *

class ArtistForm(ModelForm):
    class Meta:
        model = Artist
        exclude = ('photo')

class MultipleTextFieldWidget(Widget):
    class Media:
        js = ('scripts/multitextfield.js',)

    def render(self, name, value, attrs=None,choices=()):
        inputs = "<div class='multitext' value='"+name+"'><input class='choices' type='hidden' value='"+simplejson.dumps(dict(self.choices))+"' />"
        inputs += "[<a class='remove' href='#'> - </a>][<a class='add' href='#'> + </a>]<br/><br/>"
        #options = self.render_textfields(choices, value)
        #print options
        labels = dict(self.choices)
        #print labels
        for val in value:
            inputs += "<input name='"+name+"Name' type='text' value='"+str(labels[int(val)])+"'/>"
            inputs += "<input name='"+name+"' type='hidden' value='"+str(val)+"' /><br/>"
        #inputs +="<input class='return' name='"+name+"' type='hidden' value=''/>"
        #print inputs
        return mark_safe(inputs+"</div>")

class MultipleTextField(forms.models.ModelMultipleChoiceField):
    widget = MultipleTextFieldWidget
    pass

class AlbumForm(ModelForm):
    def __init__(self,*args, **kwargs):
        super(AlbumForm,self).__init__(*args,**kwargs)
        #print self.fields['artists']
        self.fields['artists'] = MultipleTextField(Artist.objects)
        #print self.fields['artists']
    class Meta:
        model = Album
        exclude = ('photos','tags')
        widgets = {
            #'artists':MultipleTextFieldWidget()
        }

class ReleaseForm(ModelForm):
    label = forms.CharField(required=False)

    class Meta:
        model = Release
        exclude = ('torrents','label')

        widgets = (
            {'album':forms.HiddenInput()}
        )

class FormatForm(ModelForm):
    class Meta:
        model = AlbumFormat
        exclude = ('torrent')
        widgets = (
            {'release':forms.HiddenInput()}
        )