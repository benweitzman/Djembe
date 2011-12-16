from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.contrib.auth.views import login

def index(request):
    c = RequestContext(request)
    if request.user.is_authenticated():
        return render_to_response('index.html',c)
    else:
        return login(request)


        