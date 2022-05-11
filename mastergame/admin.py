from django.contrib import admin

from .models import User
# Register your models here.

# tells Django admin app to allow us to manipulate Users
admin.site.register(User)