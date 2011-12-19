from twisted.internet import threads
from django.contrib.auth.models import User
from forum.models import *
from userprofile.models import *
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.db.models import Count, Max
from django.shortcuts import render_to_response

def index(request):
    forums = dict()
    for category in CATEGORIES:
        catForums = Forum.objects.filter(
            category=category[0]
        ).annotate(
            Count('threads__posts',distinct=True),
            Count('threads',distinct=True)
        )
        forums[category[1]] = catForums
    return render_to_response("forums/index.html",context_instance=RequestContext(request,{"forums":forums}))

def viewForum(request,forum_name):
    forum = Forum.objects.get(title=forum_name)
    threads = Thread.objects.annotate(
        latest_post=Max("posts__datePosted")
    ).annotate(
        Count("posts")
    ).order_by(
        "-latest_post"
    )[:25]
    return render_to_response("forums/viewForum.html",context_instance=RequestContext(request,{"forum":forum,
                                                                                               "threads":threads}))

def viewThread(request,forum_name,thread_name):
    thread = Thread.objects.get(title=thread_name)
    if "body" in request.POST:
        recentPost = Post.objects.latest("datePosted")
        if recentPost.poster == request.user:
            recentPost.text += '\n\n'+request.POST['body']
            recentPost.editor = request.user
            recentPost.save()
        else:
            newPost = Post.objects.create(poster=request.user)
            newPost.text = request.POST['body']
            newPost.save()
            thread.posts.add(newPost)
            thread.save()
    return render_to_response("forums/viewThread.html",context_instance=RequestContext(request,{"thread":thread}))