from django.contrib import admin
from .models import Users
# Register your models here.

class AdminUsers(admin.ModelAdmin):

     list_display =  ["name","email","created_at"]

admin.site.register(Users,AdminUsers)