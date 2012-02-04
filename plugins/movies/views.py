from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response
from photo.forms import PhotoForm
from plugins.movies.models import *

def filmsIndex(request):
    films = Movie.objects.all()
    return render_to_response('movies/films/index.html',context_instance=RequestContext(request,{"films":films}))

def filmPage(request,film_id):
    movie = Movie.objects.get(id=film_id)
    photoform = PhotoForm()
    if request.POST:
        if "photoform" in request.POST:
            photoform = PhotoForm(request.POST)
            if photoform.is_valid():
                photo = photoform.save()
                movie.photos.add(photo)

    return render_to_response('movies/films/viewFilm.html',context_instance=RequestContext(request,{"film":movie,
                                                                                                    "photoform":photoform}))

def peopleIndex(request):
    people = Person.objects.all()
    return render_to_response('movies/people/index.html',context_instance=RequestContext(request,{"people":people}))