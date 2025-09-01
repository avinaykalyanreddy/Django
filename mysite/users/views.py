

from django.contrib.messages import success,error
from django.shortcuts import render, redirect
from django.template.loader import render_to_string

from .forms import  UserSignUp
from .models import  Users
from django.http import HttpResponse
from django.contrib.auth.hashers import make_password
from uuid import uuid4

from django.core.mail import EmailMessage




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

                #m = success(reqeust, f"{user_object.name} your account is created")

                #return redirect("users:login")
                return HttpResponse("Mail sent Successful")


        return render(reqeust, "users/sign_up.html", {"form": form})

    form = UserSignUp()

    return render(reqeust,"users/sign_up.html",{"form":form})

def login(request):

    return HttpResponse("Hello user")


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

            return HttpResponse("mail Verified")

    return HttpResponse("Verification Link is expired")