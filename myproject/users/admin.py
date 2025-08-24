from django.contrib import admin
from .models import UserDetails,UserProfilePic
# Register your models here.

admin.site.register(UserDetails)

admin.site.register(UserProfilePic)