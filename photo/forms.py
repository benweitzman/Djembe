from django.forms import ModelForm
from photo.models import Photo

class PhotoForm(ModelForm):

    class Meta:
        model = Photo