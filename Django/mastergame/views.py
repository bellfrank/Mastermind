# Django authentication functions
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django import forms
from django.shortcuts import render
from django.urls import reverse
import datetime

#import Models
from .models import User


# Django Form
class NewTaskForm(forms.Form):
    task = forms.CharField(label="New Task")
    number = forms.IntegerField(label="Number", min_value=0, max_value=7)

# Homepage, two pathways, guest and logged in user. Request is an object that gets passed in
def index(request):

    # PATHWAY 1 (GUEST)
    if not request.user.is_authenticated:
        # look inside session to see if list of tasks exists, if not, create one, Django keeps info regarding sessions -> tables
        if "tasks" not in request.session:
            request.session["tasks"] = []

        return render(request, "mastergame/index.html",{
            "now": datetime.datetime.now(),
            "tasks": request.session["tasks"],
            "form": NewTaskForm()
        })

    # PATHWAY 2 (USER LOGGED IN)
    if request.user.is_authenticated:

        if "tasks" not in request.session:
            request.session["tasks"] = []

        return render(request, "mastergame/index.html",{
            "now": datetime.datetime.now(),
            "tasks": request.session["tasks"],
            "form": NewTaskForm()
        })



def add(request):
    if request.method == "POST":
        # creates an empty form and fills it with user input
        form = NewTaskForm(request.POST)
        if form.is_valid():
            # allows us to take field from form and dynamically grow our global variable tasks
            task = form.cleaned_data["task"]
            # appending the task to the list
            request.session["tasks"] += [task]
            # trying to not harcode redirections is better in case name changes
            return HttpResponseRedirect(reverse("mastergame:index"))
        else:
            # simply returning the existing form 
            return render(request, "mastergame/index.html",{
                "form": form
            })
    
    return render(request, "mastergame/index.html",{
        "form": NewTaskForm
    })


def login_view(request):
    if request.method == "POST":

        # Accessing username and password from form data
        username = request.POST["username"]
        password = request.POST["password"]

         # Check if username and password are correct, returning User object if so
        user = authenticate(request, username=username, password=password)
        
        # If user object is returned, log in and route to index page:
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("mastergame:index"))
        # Otherwise, return login page again with new context
        else:
            return render(request, "mastergame/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "mastergame/login.html")

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("mastergame:index"))

def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "mastergame/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "mastergame/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("mastergame:index"))
    else:
        return render(request, "mastergame/register.html")