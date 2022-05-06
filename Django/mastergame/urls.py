from django.urls import path
from . import views


# avoid namespace collisions
app_name = "mastergame"
urlpatterns = [
    path("<str:name>", views.index, name="index")
]