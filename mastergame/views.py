# Django authentication functions
from glob import glob
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django import forms
from django.shortcuts import render
from django.core.mail import send_mail
from django.urls import reverse
import datetime
from numpy import number
import requests
import time

# import helper function
from helpers import numcheck, combinations

# import Models
from .models import User

# Global Variables
API_CALL = False
numbers = []

# Debug ON/OFF
DEBUG = True

# Homepage, two pathways, guest and logged in user. Request is an object that gets passed in
def index(request):
    
    # PATHWAY 1 (GUEST USER)
    if not request.user.is_authenticated:
        # look inside session to see if session variables exist, if not, create one, Django keeps info regarding sessions in tables
        if "combinations" not in request.session:
            request.session["combinations"] = []
        if "attempts" not in request.session:
            request.session["attempts"] = 10
        if "score" not in request.session:
            request.session["score"] = 0

        return render(request, "mastergame/index.html",{
            "now": datetime.datetime.now(),
            "combinations": request.session["combinations"],
            "attempts": request.session["attempts"],
            "score": request.session["score"]
        })

    
    # PATHWAY 2 (USER LOGGED IN)
    if request.user.is_authenticated:

        if "user_combinations" not in request.session:
            request.session["user_combinations"] = []
        if "user_attempts" not in request.session:
            request.session["user_attempts"] = 10
        if "user_score" not in request.session:
            request.session["user_score"] = 0

        return render(request, "mastergame/index.html",{
            "now": datetime.datetime.now(),
            "combinations": request.session["user_combinations"],
            "attempts": request.session["user_attempts"],
            "score": request.session["user_score"]
        })


def add(request):
    # Global variables
    global API_CALL
    global numbers

    # Request 4 RANDOM integers from API (fetched once per game)
    if not API_CALL:
        response = requests.get('https://www.random.org/integers/?num=4&min=0&max=7&col=1&base=10&format=plain&rnd=new')
        numbers = response.text
        API_CALL = True
    
    # Debug
    if DEBUG:
        print("API Numbers: ", numbers[0], numbers[2], numbers[4], numbers[6])

    # If user submits 4 digits
    if request.method == "POST":
        guess_counter = 0
       
        comb1 = int(request.POST["number1"])
        comb2 = int(request.POST["number2"])
        comb3 = int(request.POST["number3"])
        comb4 = int(request.POST["number4"])
        
        numbers_copy = []

        k = 0
        for num in numbers:
            if(num == '\n'):
                continue
            numbers_copy.append(int(num))
            k += 1


        # Backend 4 digit validation
        if not numcheck(comb1) or not numcheck(comb2) or not numcheck(comb3) or not numcheck(comb4):
            return render(request, "mastergame/index.html",{
            "now": datetime.datetime.now(),
            "message": "invalid input",
            "combinations": request.session["combinations"],
            "attempts": request.session["attempts"],
            "score": request.session["score"]
        })
    
        # Checking user input against API number and generates feedback

        if comb1 == int(numbers[0]) and comb2 == int(numbers[2]) and comb3 == int(numbers[4]) and comb4 == int(numbers[6]):
            guess_message = "Well done! You guessed the correct number :)"
            request.session["score"] += 1
            request.session["attempts"] = 10
            request.session["combinations"] = []
            API_CALL = False
            
            return render(request, "mastergame/index.html",{
            "now": datetime.datetime.now(),
            "combinations": request.session["combinations"],
            "attempts": request.session["attempts"],
            "score": request.session["score"],
            "guess_message": guess_message,
        })

        # N numbers correct and the right location
        flag1 = False
        flag2 = False
        flag3 = False
        flag4 = False

        if(comb1 == int(numbers[0])):
            guess_counter += 1
            flag1 = True
        if(comb2 == int(numbers[2])):
            guess_counter +=1
            flag2 = True
        if(comb3 == int(numbers[4])):
            guess_counter += 1
            flag3 = True
        if(comb4 == int(numbers[6])):
            guess_counter += 1
            flag4 = True
        
        
        # If you guessed correct numbers but in the wrong location
        # searching the list and if the user's input is in the list
        guess_counter2 = 0
        
        if not flag1 and comb1 in numbers_copy:
            guess_counter2 += 1
        if not flag2 and comb2 in numbers_copy:
            guess_counter2 += 1
        if not flag3 and comb3 in numbers_copy:
            guess_counter2 += 1
        if not flag4 and comb4 in numbers_copy:
            guess_counter2 += 1
        

        guess_message = f"You have guessed {guess_counter} numbers correctly and their right location! :)" + f"You also guessed {guess_counter2} numbers correctly but not in their right location!"

        if guess_counter == 0 and guess_counter2 == 0:
            guess_message = "Your guess was incorrect :("

        # Add user guess to history of guesses
        request.session["combinations"] += [f"{comb1}  {comb2}  {comb3}  {comb4} - {guess_message}"]
        request.session["attempts"] -= 1

        
        return render(request, "mastergame/index.html",{
            "now": datetime.datetime.now(),
            "combinations": request.session["combinations"],
            "attempts": request.session["attempts"],
            "score": request.session["score"],
            "guess_message": guess_message,
        })
    
    else:
        return render(request, "mastergame/index.html")


def reset(request):
    # resets number by allowing API to get called again, once
    global API_CALL
    API_CALL = False
    if request.user.is_authenticated:
        request.session["user_combinations"] = []
        request.session["user_attempts"] = 10
        request.session["user_score"] = 0
        
        return HttpResponseRedirect(reverse("mastergame:index"))

    else:
        request.session["combinations"] = []
        request.session["attempts"] = 10
        request.session["score"] = 0
        
        return HttpResponseRedirect(reverse("mastergame:index"))



def settings(request):
    return render(request, "mastergame/settings.html")

def leaderboard(request):
    return render(request, "mastergame/leaderboards.html")


########################## USER REGISTRATION  ############################################

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