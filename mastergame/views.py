# Django authentication functions
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django import forms
from django.shortcuts import render
from django.core.mail import send_mail
from django.urls import reverse
import datetime

#import Models
from .models import User

# Homepage, two pathways, guest and logged in user. Request is an object that gets passed in
def index(request):

    # PATHWAY 1 (GUEST USER)
    if not request.user.is_authenticated:
        # look inside session to see if list of tasks exists, if not, create one, Django keeps info regarding sessions -> tables
        if "combinations" not in request.session:
            request.session["combinations"] = []
        if "attempts" not in request.session:
            request.session["attempts"] = 10
        if "score" not in request.session:
            request.session["score"] = 0

        return render(request, "mastergame/index.html",{
            "now": datetime.datetime.now(),
            "tasks": request.session["combinations"],
            "attempts": request.session["attempts"],
            "score": request.session["score"]
        })

    
    # PATHWAY 2 (USER LOGGED IN)
    if request.user.is_authenticated:

        if "combinations2" not in request.session:
            request.session["combinations2"] = []

        return render(request, "mastergame/index.html",{
            "now": datetime.datetime.now(),
            "tasks": request.session["combinations2"]
        })


def add(request):
    if request.method == "POST":
       
        comb1 = int(request.POST["number1"])
        comb2 = int(request.POST["number2"])
        comb3 = int(request.POST["number3"])
        comb4 = int(request.POST["number4"])

        if comb1 == 1:
            if comb2 == 2:
                if comb3 == 3:
                    if comb4 == 4:
                        request.session["score"] += 1
                        return render(request, "mastergame/index.html", {
                            "message": "NICE!",
                            "now": datetime.datetime.now(),
                            "tasks": request.session["combinations"],
                            "attempts": request.session["attempts"],
                            "score": request.session["score"]
                        })

        # Backend validation
        if comb1 < 0 or comb1 > 7:
            return HttpResponseRedirect(reverse("mastergame:index"),{
                "message":"helo"
            })
            

        # appending the combination to dynamic list
        if request.user.is_authenticated:
            request.session["combinations2"] += [[comb1, comb2, comb3, comb4]]
        else:
            request.session["combinations"] += [[comb1, comb2, comb3, comb4]]
            request.session["attempts"] -= 1

        # trying to not harcode redirections is better in case name changes
        return HttpResponseRedirect(reverse("mastergame:index"))
        # else:
        #     # simply returning the existing form 
        #     return HttpResponseRedirect(reverse("mastergame:index"))
    
    return render(request, "mastergame/index.html")



def reset(request):
    if not request.user.is_authenticated:
        # look inside session to see if list of tasks exists, if not, create one, Django keeps info regarding sessions -> tables
        if "combinations" in request.session:
            request.session["combinations"] = []
        if "attempts" in request.session:
            request.session["attempts"] = 10
        if "score" in request.session:
            request.session["score"] = 0
        
        return HttpResponseRedirect(reverse("mastergame:index"))
    else:
        if "combinations2" in request.session:
            request.session["combinations"] = []
        if "attempts" in request.session:
            request.session["attempts"] = 10
        return HttpResponseRedirect(reverse("mastergame:index"))




# USER REGISTRATION CODE
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

@login_required
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("mastergame:index"))

def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        if not username:
            return render(request, "mastergame/register.html", {
                "message": "Username cannot be left blank."
            })
        if not email:
            return render(request, "mastergame/register.html", {
                "message": "Email cannot be left blank."
            })

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]

        if not password:
            return render(request, "mastergame/register.html", {
                "message": "Password cannot be left blank."
            })

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




# def contact(request):
#     if request.method == "POST":
#         message_name = request.POST['message-name']
#         message_email = request.POST['message-email']
#         message = request.POST['message']

#         #send an email
#         send_mail(
#             message_name, # subject
#             message, # message
#             message_email, # from email
#             ['franciscocw0101@gmail.com'], # To email
#         )

#         return render(request, 'mastergame/contact.html')
    
#     else:
#         return render(request, "mastergame/contact.html")