from django.contrib.auth.models import User
from userprofile.models import *
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response

def mine(request):
    showuser = request.user
    return render_to_response("profile/view.html",context_instance=RequestContext(request,{"showuser":showuser}))

def view(request,username=""):
    if "username" in request.GET:
        return HttpResponseRedirect("/user/"+request.GET["username"])
    showuser = User.objects.get(username=username)
    return render_to_response("profile/view.html",context_instance=RequestContext(request,{"showuser":showuser}))

def editProfile(request):
    if request.POST:
        user = User.objects.get(id=request.user.id)
        f = ProfileForm(request.POST,instance=user.get_profile())
        """csi = ""
        for i in dict(f.data)['megasearch']:
            csi += i+","
        f.data.__setitem__("megasearch",csi)"""
        if f.is_valid():
            u = f.save(commit=False)
            csi = ""
            for i in dict(f.data)['megasearch']:
                csi += i+","
            u.megasearch = csi
            u.save()
            return HttpResponseRedirect("/profile/mine")
    user = User.objects.get(id=request.user.id)
    form = ProfileForm(instance=user.get_profile())
    c = RequestContext(request,{"form":form})
    return render_to_response("profile/edit.html",c)