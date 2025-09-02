
from django.urls import path
from . import views

app_name = "users"


urlpatterns = [

    path("signup/",views.sign_up,name="signup"),

    path("login/",views.login,name="login"),

    path("verifying/",views.checking_email_verification,name="checking_email_verification"),

    path("logout/",views.logout,name="logout"),

]