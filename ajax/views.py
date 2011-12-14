from django.http import HttpResponse
from django.utils import simplejson
from groups.models import *

def index(request):
    message= "[]"
    if request.is_ajax():
        kind = request.GET['kind']
        model = Artist
        if kind == "Artist":
            model = Artist
        elif kind == "Album":
            model = Album
        #a = Artist.objects.filter(name__startswith=request.POST['letters'])
        letters = request.GET['letters']
        a = model.objects.values('name').filter(name__startswith=letters)
        if a:
            message = simplejson.dumps(list(a))
    return HttpResponse(message)
