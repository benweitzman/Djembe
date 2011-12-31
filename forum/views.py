from twisted.internet import threads
from django.contrib.auth.models import User
from forum.models import *
from userprofile.models import *
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.db.models import Count, Max
from django.shortcuts import render_to_response
from django.core.paginator import Paginator

def index(request):
    forums = dict()
    for category in CATEGORIES:
        catForums = Forum.objects.filter(
            category=category[0]
        ).annotate(
            Count('threads__posts',distinct=True),
            Count('threads',distinct=True)
        )
        for i in catForums:
            i.latest_thread = i.get_latest()
            if i.latest_thread:
                i.pages = i.latest_thread.posts__count/request.user.get_profile().postsPerPage
                try:
                    lastRead = ThreadView.objects.get(user=request.user,thread=i.latest_thread)
                    i.lastRead = lastRead.post_id
                except ThreadView.DoesNotExist:
                    i.lastRead = 0
            else:
                i.pages = 0
                i.lastRead = 0
        forums[category[1]] = catForums
    return render_to_response("forums/index.html",context_instance=RequestContext(request,{"forums":forums}))

def viewPost(request,post_id):
    post = Post.objects.get(id=post_id)
    page = post.index/request.user.get_profile().postsPerPage
    thread = post.thread_set.get()
    forum = thread.forum_set.get()
    return HttpResponseRedirect("/forums/thread/"+str(thread.id)+"/"+str(page+1)+"#post"+str(post_id))

def viewForum(request,forum_id):
    forum = Forum.objects.get(id=forum_id)
    if "newThread" in request.POST:
        newThread = Thread.objects.create(title=request.POST['title'],op=request.user)
        newPost = Post.objects.create(poster=request.user,index=0)
        newPost.text = request.POST['body']
        newPost.save()
        newThread.posts.add(newPost)
        newThread.save()
        forum.threads.add(newThread)
        forum.save()
        return HttpResponseRedirect(newThread.get_absolute_url())
    threads = Thread.objects.filter(
        forum=forum
    ).annotate(
        latest_post=Max("posts__datePosted")
    ).annotate(
        Count("posts")
    ).annotate(
        pages=Count("posts",distinct=True)
    ).order_by(
        "-latest_post"
    )[:25]
    for i in threads:
        i.pages = i.pages/request.user.get_profile().postsPerPage
        try:
            lastRead = ThreadView.objects.get(user=request.user,thread=i)
            i.lastRead = lastRead.post_id
        except ThreadView.DoesNotExist:
            i.lastRead = 0
    return render_to_response("forums/viewForum.html",context_instance=RequestContext(request,{"forum":forum,
                                                                                               "threads":threads}))

def viewThread(request,thread_id,page=1):
    thread = Thread.objects.annotate(Count("posts")).get(id=thread_id)
    p = Paginator(thread.posts.all(),request.user.get_profile().postsPerPage)
    showpages = 9
    startpage = 0
    stoppage = p.num_pages
    if stoppage>showpages:
        startpage=int(page)-round(showpages/2)-1
        if startpage <= 0:
            startpage = 0
        elif startpage >= p.num_pages-showpages:
            startpage = p.num_pages-showpages
        stoppage=startpage+showpages
    pages = map(lambda x: p.page(x),p.page_range)
    showPages = dict(enumerate(pages[int(startpage):int(stoppage)]))
    posts = p.page(page)
    lastPost = posts[-1]
    try:
        threadView = ThreadView.objects.get(user=request.user,thread=thread)
        if lastPost.id > threadView.post_id:
            threadView.post = lastPost
            threadView.save()
    except ThreadView.DoesNotExist:
        threadView = ThreadView.objects.create(user=request.user,thread=thread,post=lastPost)
        threadView.save()
    if "body" in request.POST:
        recentPost = []
        if thread.posts.all():
            recentPost = thread.posts.latest("datePosted")
        if recentPost and recentPost.poster == request.user:
            recentPost.text += '\n\n'+request.POST['body']
            recentPost.editor = request.user
            recentPost.save()
        else:
            newPost = Post.objects.create(poster=request.user,index=thread.posts__count)

            newPost.text = request.POST['body']
            newPost.save()
            thread.posts.add(newPost)
            thread.save()
    return render_to_response("forums/viewThread.html",context_instance=RequestContext(request,{"thread":thread,
                                                                                                "pages":pages,
                                                                                                "posts":posts,
                                                                                                "showPages":showPages,
                                                                                                "startPage":startpage,
                                                                                                "stopPage":stoppage,}))