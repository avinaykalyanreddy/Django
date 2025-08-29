from django.http import HttpResponse
from django.shortcuts import render,redirect
from .forms import UserSignUpForm,UserLoginForm,UserResetPassword
from .models import UserDetails

from django.contrib.auth import hashers
# Create your views here.

from .decorators import login_required_custom

@login_required_custom
def home(request):

    return render(request,"users/home.html")


def signup(request):
    if request.method == "POST":
        form = UserSignUpForm(request.POST)
        if form.is_valid():
            password = form.cleaned_data["current_password"]
            user = form.save(commit=False)
            user.user_password = hashers.make_password(password)
            user.save()
            return redirect("users:login")
        return render(request, "users/signup.html", {"form": form})

    return render(request, "users/signup.html", {"form": UserSignUpForm()})

def login(request):

    if request.method == "POST":

        form = UserLoginForm(request.POST)

        if form.is_valid():

            username = form.cleaned_data.get("username")


            obj = UserDetails.objects.filter(user_name=username).first()

            user_id = obj.id

            request.session["user_id"] = user_id
            request.session["username"] = username


            return redirect("users:home")

        return render(request,"users/login.html",{"form":form})


    form = UserLoginForm()
    return render(request,"users/login.html",{"form":form})


def logout(request):

    request.session.flush()

    return redirect("users:login")

@login_required_custom
def reset_password(request, id):

    if request.method == "POST":
        form = UserResetPassword(request.POST)  # Use request.POST

        if form.is_valid():
            obj = UserDetails.objects.get(id=id)
            obj.user_password = hashers.make_password(form.cleaned_data.get("new_password"))
            obj.save()
            return redirect("users:login")

        return render(request, "users/reset_password.html", {"form": form})

    form = UserResetPassword(initial={"user_id": id})
    return render(request, "users/reset_password.html", {"form": form})

