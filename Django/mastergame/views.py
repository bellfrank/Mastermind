from django.http import HttpResponse, HttpResponseRedirect
from django import forms
from django.shortcuts import render
from django.urls import reverse
import datetime


# Django Form
class NewTaskForm(forms.Form):
    task = forms.CharField(label="New Task")
    number = forms.IntegerField(label="Number", min_value=0, max_value=7)

# Homepage
def index(request, name):
    #looking inside the session to see if theres a list of tasks, if not create one
    # django stores information about sessions in tables, we need to create one using
    # python3 manage.py migrate
    if "tasks" not in request.session:
        request.session["tasks"] = []

    if request.method == "POST":
        add(request, name)
    return render(request, "mastergame/index.html",{
        "name": name.capitalize(),
        "now": datetime.datetime.now(),
        "tasks": request.session["tasks"],
        "form": NewTaskForm()
    })


def add(request, name):
    if request.method == "POST":
        # creates an empty form and fills it with user input
        form = NewTaskForm(request.POST)
        if form.is_valid():
            # allows us to take field from form and dynamically grow our global variable tasks
            task = form.cleaned_data["task"]
            # appending the task to the list
            request.session["tasks"] += [task]
            # trying to not harcode redirections is better in case name changes
            return HttpResponseRedirect(reverse("mastergame:index", args=(name,)))
        else:
            # simply returning the existing form 
            return render(request, "mastergame/index.html",{
                "form": form
            })
    
    return render(request, "mastergame/index.html",{
        "form": NewTaskForm
    })