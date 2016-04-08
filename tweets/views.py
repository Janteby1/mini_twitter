from django.shortcuts import render, redirect
from django.views.generic import View
from django.http import HttpResponse, HttpResponseForbidden, JsonResponse
from django.db.models import Q

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
import json

from .forms import UserForm, LoginForm, CreateForm
from .models import UserProfile, Tweet

 
# Create your views here.
class Index(View):
    def get(self, request):
        user_form = UserForm()
        login_form = LoginForm()
        create_form = CreateForm()

        context = {
            'user_form': user_form,
            "login_form":login_form,
            "create_form": create_form,
            }

        return render(request, "index.html", context)


class Register(View):
    def post(self, request):
        if request.is_ajax():
            data = request.POST
        else:
            body = request.body.decode()
            if not body: 
                return JsonResponse ({"response":"Missing Body"})
            data = json.loads(body)

        user_form = UserForm(data)
        if user_form.is_valid():
            user = user_form.save()
            return JsonResponse({"Message": "Register succesfull", "success": True})
        else:
            return JsonResponse ({"response":"Invalid information"})


class Login(View):
    def post(self, request):
        if request.is_ajax():
            data = request.POST
        else:
            body = request.body.decode()
            if not body: 
                return JsonResponse ({"response":"Missing Body"})
            data = json.loads(body)

        username = data.get('username')
        password = data.get('password')
        if not (username and password):
            return JsonResponse({'Message':'Missing username or password.'})
        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:
                login(request, user) # django built in login 
                username = request.user.username
                return JsonResponse({'Message':'Welcome in!', "username":username})
            else:
                return JsonResponse({'Message':'Username is inactive'})
        else:
            return JsonResponse({'Message':'Invalid `username` or `password`.'})


class Logout(View):
    def post(self, request):
        print(request)
        logout(request) # django built in logout 
        return JsonResponse ({"Message":"Logout Successful"})


class Create_Tweet(View):
    def post(self, request):
        if not request.user.is_authenticated():
            # if there is no user logged in they can not submit a post 
            # this redirects them to a 403 html page with an error message
            return JsonResponse({'Message':'Please sign in to submit a post'})

        form = CreateForm(data=request.POST)
        if form.is_valid():
            user = request.user
            tweet = form.save(commit=False)
            tweet.user = user 
            tweet.save()

            tweets = Tweet.objects.filter(Q(user=user) | Q(repost=user)).order_by('-created_at')
            res = [tweet.to_json() for tweet in tweets]

            return JsonResponse({'Message':'Tweet submitted!','tweets': res})
        else:
            return JsonResponse ({"Message":"Invalid information"})


class Get_All(View):
    def post(self, request):
        tweets = Tweet.objects.all().order_by('-created_at')
        res = [tweet.to_json() for tweet in tweets]
        
        if res:
            return JsonResponse({"tweets": res})
        else:
            return JsonResponse ({"response":"You have no tweets"})


class Profile(View):
    def post(self, request, pk):
        # this gets back all the tweets that the pk matches the user or the pk matches a repost
        tweets = Tweet.objects.filter(Q(user=pk) | Q(repost=pk)).order_by('-created_at')
        res = [tweet.to_json() for tweet in tweets]
        
        if res:
            return JsonResponse({"tweets": res})
        else:
            return JsonResponse ({"response":"You have no tweets"})


class Repost(View):
    def post(self, request, pk):
        tweet = Tweet.objects.get(pk=pk)
        user = request.user
        tweet.repost.add(user)
        tweet.save()

        tweets = Tweet.objects.filter(Q(user=user) | Q(repost=user)).order_by('-created_at')
        res = [tweet.to_json() for tweet in tweets]

        if res:
            return JsonResponse({"tweets": res})
        else:
            return JsonResponse ({"response":"You have no tweets"})


class Up(View):
    def post(self, request, pk):
        pk = pk
        tweet = Tweet.objects.get(pk = pk)
        tweet.likes += 1
        tweet.save()

        tweets = Tweet.objects.all().order_by('-created_at')
        res = [tweet.to_json() for tweet in tweets]

        if res:
            return JsonResponse({"Message": "Voted Up!", "tweets": res})
        else:
            return JsonResponse ({"response":"Invalid information"})


class Down(View):
    def post(self, request, pk):
        pk = pk
        tweet = Tweet.objects.get(pk = pk)
        tweet.likes -= 1
        tweet.save()

        tweets = Tweet.objects.all().order_by('-created_at')
        res = [tweet.to_json() for tweet in tweets]

        if res:
            return JsonResponse({"Message": "Voted Down!", "tweets": res})
        else:
            return JsonResponse ({"response":"Invalid information"})


class Edit(View):    
    def get(self, request, pk):
        user = request.user
        tweet = Tweet.objects.get(pk = pk, user=user) #adds user constraints
        form = CreateForm(instance=tweet)

        context = {
            "tweet_id": tweet.id,
            "edit_form": form.as_p(),}
        return JsonResponse(context)

    def post(self, request, pk):
        user = request.user
        tweet = Tweet.objects.get(pk=pk)
        if not tweet:
            return JsonResponse ({"Message":"Invalid information"})
        # this time we get the form with the data
        form = CreateForm(data=request.POST, instance=tweet)

        if form.is_valid():
            tweet = form.save()

            tweets = Tweet.objects.filter(Q(user=user) | Q(repost=user)).order_by('-created_at')
            res = [tweet.to_json() for tweet in tweets]

            return JsonResponse({"Message": "Edited succesfull", "tweets": res})
        else:
            return JsonResponse ({"Message":"Invalid information"})


class Delete(View):
    def post(self, request, pk):
        user = request.user
        tweet = Tweet.objects.get(pk = pk, user=user) #adds user constraints
        tweet.delete()

        tweets = Tweet.objects.filter(Q(user=user) | Q(repost=user)).order_by('-created_at')
        res = [tweet.to_json() for tweet in tweets]

        if res:
            return JsonResponse({"Message": "Deleted", "tweets": res})
        else:
            return JsonResponse ({"response":"Invalid information"})


class Search_User(View):
    def post(self, request):
        if request.is_ajax():
            data = request.POST
        else:
            body = request.body.decode()
            if not body: 
                return JsonResponse ({"response":"Missing Body"})
            data = json.loads(body)

        username = data.get('search_value')
        user = User.objects.get(username=username)
        if not user:
            return JsonResponse({'Message':'No matches for search.'})

        tweets = Tweet.objects.filter(user=user).order_by('-created_at')
        res = [tweet.to_json() for tweet in tweets]
        if res:
            return JsonResponse({"tweets": res})
        else:
            return JsonResponse ({"response":"User have no tweets"})


class Search_Tag(View):
    def post(self, request):
        if request.is_ajax():
            data = request.POST
        else:
            body = request.body.decode()
            if not body: 
                return JsonResponse ({"response":"Missing Body"})
            data = json.loads(body)

        tag = data.get('search_value')
        if not tag:
            return JsonResponse({'Message':'No input for search.'})

        # this is not perfect, needs to match all the tags bc they are a string and no individual yet
        tweets = Tweet.objects.filter(tags=tag).order_by('-created_at')
        res = [tweet.to_json() for tweet in tweets]
        if res:
            return JsonResponse({"tweets": res})
        else:
            return JsonResponse ({"response":"User have no tweets"})












