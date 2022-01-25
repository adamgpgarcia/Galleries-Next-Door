from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, HttpResponseRedirect
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from datetime import datetime, timezone, timedelta
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, UpdateView
from django.db.models import F
from django.forms.models import model_to_dict
from .models import PostModel
from django.utils.safestring import mark_safe
from django.shortcuts import render
import math
import json


from . import models
from . import forms


def sellermessage(request, id):
    art = models.PostModel.objects.get(id=id)
    if not request.user.is_authenticated:
        return redirect("/")
    if request.method == "POST":
        if request.user.is_authenticated:
            form = forms.CommentForm(request.POST)
            if form.is_valid():
                form.save(request, post_id)
                return redirect("/")
        else:
            return redirect("/")

    form = forms.CommentForm()
    context = {
        "user": request.user,
        "post_id": id,
        "form":form,
        "seller" : art.author,
        "art" : art,
    }

    return render(request, "sellermessage.html", context=context)

def register(request):
    if request.method == "POST":
        form_instance = forms.RegistrationForm(request.POST)
        if form_instance.is_valid():
            form_instance.save()
            return redirect("/login/")
    else:
        form_instance = forms.RegistrationForm()
    context = {
        "form":form_instance,
    }
    return render(request, "registration/register.html", context=context)

def logout_view(request):
    logout(request)
    return redirect("/login/")

#Auction Views
def auctions(request):

    #li = models.Suggestion.objects.all()[page*10:page*10+10]
    li = models.PostModel.objects.filter(author=request.user).order_by(
        '-published_on'
    )
    print(li)
    # list(range(page*20, page*20+20)) example list variables change on page

    context = {
        "my_list" : li,
        "title" : "Live Auctions",
    }

    return render(request, "auction.html", context=context)

def art_bet(request, id):
    post = models.PostModel.objects.get(id=id)
    if post.current_bet_leader == request.user:
        is_you = True
    else:
        is_you = False

    context = {
        "cur_art" : post,
        "is_you" : is_you,
        "cur_id" : post.id,

    }

    return render(request, "artbet.html", context=context)

def BetOneView(request, id):
    post = models.PostModel.objects.get(id=id)
    post.current_bet += 1
    post.current_bet_leader = request.user
    post.save()
    return redirect('/auction/' + str(id) + '/')

def BetFiveView(request, id):
    post = models.PostModel.objects.get(id=id)
    post.current_bet += 5
    post.current_bet_leader = request.user
    print("User:", request.user)
    print(post.current_bet_leader)
    post.save()
    return redirect('/auction/' + str(id) + '/')


#Add, Delete, Edit Post
def add_post(request):
    if not request.user.is_authenticated:
        return redirect("/")
    print(request.method)
    if request.method == "POST":
        if request.user.is_authenticated:
            form = forms.PostForm(request.POST, request.FILES)
            if form.is_valid():
                form.save(request)
                return redirect("/")
        else:
            return redirect("/")
    else:
        form = forms.PostForm()

    context = {
        "title":"Add Art",
        "form":form
    }
    return render(request, "post.html", context=context)

def UpdatePost(request, id):
    post = models.PostModel.objects.get(id=id)
    form = forms.PostUpdateForm(initial=model_to_dict(post))

    if request.method == "POST":

        form = forms.PostUpdateForm(request.POST, request.FILES)
        if request.user.is_authenticated:
            if form.is_valid():

                title = form.cleaned_data['title']
                image = form.cleaned_data['image']
                image_description = form.cleaned_data['image_description']
                auction_at = form.cleaned_data['auction_at']

                if image:
                    post.image = image
                else:
                    post.image = post.image

                post.title = title
                post.image_description = image_description
                post.auction_at = auction_at
                post.save()
                return redirect("/listings/")
        else:
            print("nonvalid posted")
            return redirect("/listings/")

    context = {
        "title":"Edit Art",
        "form":form,
        "id": id,
    }

    return render(request, "edit.html", context=context)

def DeletePost(request, id):
    post = models.PostModel.objects.get(id=id)
    post.delete()
    return redirect("/listings/")


#Main Listings Views
def LikeView(request, id):

    auction_list = models.PostModel.objects.filter(auction_at__lte=F("total_likes"))
    post = models.PostModel.objects.get(id=id)

    if post.likes.filter(id = request.user.id).exists():
        post.likes.remove(request.user)
        post.total_likes -= 1
        post.save()

    else:
        post.likes.add(request.user)
        post.total_likes += 1
        post.save()

    for item in auction_list:
        if item.current_state == 0:
            item.current_state = 1;
            item.auction_start = datetime.now()
            item.save()


    return render(request, "index.html")

class index(ListView):

    model = PostModel
    template_name = "index.html"

    posts = models.PostModel.objects.all()
    # list(range(page*20, page*20+20)) example list variables change on page

    #cur = models.PostModel.objects.get(id=id)

    def get(self, request):
        if not request.user.is_authenticated:
            return redirect("/login/")
        like_list = models.PostModel.objects.filter(id=request.user.id).exists()

        info = {
            "like_list" : like_list
        }

        return render(request,self.template_name, info)


    context = {
        "my_list" : posts,
        "title" : "Gallery Listings",
    }


#Art Chat View

def art_chat(request, id):
    post = models.PostModel.objects.get(id=id)
    context = {
        "cur_art" : post,
        'room_name': id,
    }

    return render(request, "artchat.html", context=context)

def messages(request):

    sold_art = models.PostModel.objects.filter(current_state=2).filter(current_bet_leader=request.user)

    context = {
        "sell_messages" : sold_art,
        "title" : "Messages"
    }

    return render(request, "messages.html", context=context)

#Output Database to HTML

def get_posts(request):
    post_objects = models.PostModel.objects.all()

    post_list = {}
    post_list["posts"] = []
    for item in post_objects:
        comment_objects = models.CommentModel.objects.filter(title=item)
        temp_post = {}
        temp_post["id"] = item.id
        temp_post["title"] = item.title
        temp_post["author"] = item.author.username
        temp_post["date"] = item.published_on.strftime("%Y-%m-%d %H:%M:%S")     #or = datetime.now(timezone.utc) - comm.published_on
        temp_post["comments"] = []
        temp_post["auction_at"] = item.auction_at
        temp_post["total_likes"] = item.total_likes
        leader = item.current_bet_leader
        temp_post["current_bet_leader"] = str(leader)
        temp_post["liked_by_you"] = item.likes.filter(id=request.user.id).exists()
        if item.current_state == 2:
            temp_post["sold"] = True
        else:
            temp_post["sold"] = False


        try:
            temp_post["image"] = item.image.url
            temp_post["image_desc"] = item.image_description
        except Exception as err:
            print(err)
            temp_post["image"] = ""
            temp_post["image_desc"] = ""

        for comm in comment_objects:
            temp_comm = {}
            temp_comm["id"] = comm.id
            temp_comm["comment"] = comm.comment
            temp_comm["author"] = comm.author.username
            temp_comm["date"] = comm.published_on.strftime("%Y-%m-%d %H:%M:%S") #datetime.now(timezone.utc) - comm.published_on  timer of time since posted
            temp_post["comments"].append(temp_comm)


        post_list["posts"].append(temp_post)


    return JsonResponse(post_list)

def live_auctions(request):


    post_objects = models.PostModel.objects.filter(current_state = 1).order_by(
        '-total_likes'
    )
    post_list = {}
    post_list["posts"] = []
    for item in post_objects:
        comment_objects = models.CommentModel.objects.filter(title=item)
        temp_post = {}
        temp_post["id"] = item.id
        temp_post["title"] = item.title
        temp_post["author"] = item.author.username
        temp_post["date"] = item.published_on.strftime("%m %d, %Y %H:%M:%S")     #or = datetime.now(timezone.utc) - comm.published_on
        temp_post["comments"] = []
        temp_post["auction_at"] = item.auction_at
        temp_post["total_likes"] = item.total_likes
        end = item.auction_start
        now = datetime.now()
        timez_end = end.replace(tzinfo=None)
        timez_now = now.replace(tzinfo=None)
        countdown = timez_end - timez_now

        hours, remainder = divmod(countdown.seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        seconds += countdown.microseconds / 1e6
        seconds = int(seconds)
        if hours < 10:
             hours = "0" + str(hours)
        if minutes < 10:
             minutes = "0" + str(minutes)
        if seconds < 10:
             seconds = "0" + str(seconds)

        temp_post["auction_end"] = str(hours) + " hours " + str(minutes) + " minutes " + str(seconds) + " seconds"

        if countdown.days == -2:
            item.current_state = 2
            item.save()

        try:
            temp_post["image"] = item.image.url
            temp_post["image_desc"] = item.image_description
        except Exception as err:
            print(err)
            temp_post["image"] = ""
            temp_post["image_desc"] = ""

        for comm in comment_objects:
            temp_comm = {}
            temp_comm["id"] = comm.id
            temp_comm["comment"] = comm.comment
            temp_comm["author"] = comm.author.username
            temp_comm["date"] = comm.published_on.strftime("%Y-%m-%d %H:%M:%S") #datetime.now(timezone.utc) - comm.published_on  timer of time since posted
            temp_post["comments"].append(temp_comm)


        post_list["posts"].append(temp_post)


    return JsonResponse(post_list)

def listings(request,page=0):
    if request.user.is_authenticated:
        form_instance = forms.PostForm(request.POST)
        if request.method == "POST":
            if form_instance.is_valid():
                form_instance.save(request)
                form_instance = forms.PostForm()
    else:
        form_instance = forms.PostForm()

    #li = models.Suggestion.objects.all()[page*10:page*10+10]
    li = models.PostModel.objects.filter(author=request.user).order_by(
        '-published_on'
    )
    # list(range(page*20, page*20+20)) example list variables change on page

    context = {
        "my_list" : li,
        "title" : "Your Listings",
        "form" : form_instance,
    }

    return render(request, "listings.html", context=context)

def add_comment(request, post_id):
    if not request.user.is_authenticated:
        return redirect("/")
    if request.method == "POST":
        if request.user.is_authenticated:
            form = forms.CommentForm(request.POST)
            if form.is_valid():
                form.save(request, post_id)
                return redirect("/")
        else:
            return redirect("/")

    form = forms.CommentForm()
    context = {
        "title":"Comment",
        "post_id": post_id,
        "form":form
    }
    return render(request, "comment.html", context=context)
