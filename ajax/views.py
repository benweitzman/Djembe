from django.http import HttpResponse
from django.utils import simplejson
from groups.models import *
from django.contrib.auth.models import User

def index(request):
    message= "[]"
    if request.is_ajax():
        kind = request.GET['kind']
        letters = request.GET['letters']
        model = Artist
        if kind == "Artist":
            model = Artist
            a = model.objects.values('name').filter(name__startswith=letters)
        elif kind == "Album":
            model = Album
            a = model.objects.values('name').filter(name__startswith=letters)
        elif kind == "User":
            a = User.objects.values('username').filter(username__startswith=letters)
        if a:
            message = simplejson.dumps(list(a))
    return HttpResponse(message)
