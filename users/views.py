

from django.contrib.messages import success,error
from django.shortcuts import render, redirect,reverse
from django.template.loader import render_to_string

from .forms import UserSignUp, UserLogin
from .models import  Users
from django.http import HttpResponse
from django.contrib.auth.hashers import make_password,check_password
from uuid import uuid4

from django.core.mail import EmailMessage


def index(request):

    pass


def sign_up(reqeust):

    if reqeust.method == "POST":

        form = UserSignUp(reqeust.POST)


        if form.is_valid():

            user_object = form.save(commit=False)

            password = form.cleaned_data.get("password",None)

            if password:



                user_object.password = make_password(password)
                uuid  = str(uuid4())

                user_object.token = uuid

                user_object.save()




                sending_verification_mail(uuid,user_object)


                success(reqeust, f"Verification email has been sent successfully to {user_object.email}. Please check your inbox to verify your account.")

                return redirect("users:login")


        return render(reqeust, "users/sign_up.html", {"form": form})

    form = UserSignUp()

    return render(reqeust,"users/sign_up.html",{"form":form})

def login(request):

    if request.method == "POST":
        form = UserLogin(request.POST)
        email = request.POST.get("email")
        password = request.POST.get("password")

        user = Users.objects.filter(email=email).first()

        if user :

            if check_password(password,user.password) :
                request.session["user_id"] = user.id

                success(request,"Login successful")
                return redirect("myapp:home")


            form.add_error("password","Incorrect password")

        else:
            form.add_error("email","No account found with this email address")

        return render(request, "users/login.html", {"form": form})

    form = UserLogin()

    return render(request,"users/login.html",{"form":form})

def logout(request):

    request.session.flush()
    success(request,"Logout successful")
    return redirect("myapp:home")

def sending_verification_mail(uuid,user):

    try:

        uuid_name = uuid+str(user.id)
        subject = "Verification Email for SignUp"

        html_message = render_to_string("users/email/verification_email.html",{"unique_name":uuid_name,"user":user})

        mail = EmailMessage(subject=subject,body=html_message,from_email="godsons12072004@gmail.com",to=[user.email])

        mail.content_subtype="html"

        mail.send()

        return True


    except:

        return HttpResponse("Mail server Issue,try later")


def checking_email_verification(request):

    uuid = request.GET.get("uuid")

    if uuid:
        original_uuid = uuid[:36]
        user_id = int(uuid[36::])

        user_obj = Users.objects.filter(id=user_id).first()

        if user_obj.token == original_uuid:

            user_obj.is_verified = True
            user_obj.token = uuid4()
            user_obj.save()

            return HttpResponse(f"mail Verified. Please <a href='{reverse('users:login')}' >Login</a>")

    return HttpResponse("Verification Link is expired")