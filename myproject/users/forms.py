
from django import forms
from users import models
from .models import UserDetails
from django.contrib.auth import hashers


class UserSignUpForm(forms.ModelForm):

    current_password = forms.CharField(max_length=40,widget=forms.PasswordInput(attrs={"placeholder":"Enter password"}))
    conformation_password = forms.CharField(max_length=40,widget=forms.PasswordInput(attrs={"placeholder":"Enter conform password"}))


    class Meta:

        model = models.UserDetails
        fields = ["user_name","user_email"]

    def clean_user_name(self):
        username = self.cleaned_data.get("user_name")

        if UserDetails.objects.filter(user_name=username).exists():
            self.add_error("user_name", "Username already exists")
        if " " in username:
            self.add_error("user_name", "Username contains space")

        return username

    def clean_user_email(self):
        email = self.cleaned_data.get("user_email")

        if UserDetails.objects.filter(user_email=email).exists():
            self.add_error("user_email", "Email already exists")

        return email

    def clean(self):
        cleaned_data = super().clean()
        pass1 = cleaned_data.get("current_password")
        pass2 = cleaned_data.get("conformation_password")

        if pass1 and pass2 and pass1 != pass2:
            self.add_error("conformation_password", "Both passwords should be the same")

        return cleaned_data



class UserLoginForm(forms.Form):

    username = forms.CharField(max_length=50)
    password = forms.CharField(max_length=40,
                               widget=forms.PasswordInput(attrs={"placeholder":"Enter password"}))


    def clean_username(self):
        username = self.cleaned_data.get("username")
        obj = UserDetails.objects.filter(user_name=username).exists()

        if not obj:

            self.add_error("username","user not exists")



        return username

    def clean_password(self):

        username = self.cleaned_data.get("username")
        obj = UserDetails.objects.filter(user_name=username).first()

        if obj:
            input_password = self.cleaned_data.get("password")

            password = obj.user_password

            if not hashers.check_password(input_password,password):

                self.add_error("password","Incorrect password")



            return "hashed password"
        self.add_error("password","username or incorrect password ")
        return None

class UserResetPassword(forms.Form):

    user_id = forms.IntegerField( label="",widget=forms.NumberInput(attrs={"style":'display:none;'}))

    password = forms.CharField(max_length=40, widget= forms.PasswordInput(attrs={"placeholder":"Enter Password"}))

    new_password = forms.CharField(max_length=40,label="New password")

    conform_password  = forms.CharField(max_length=40,label="Conform password")

    def clean_password(self):

        password = self.cleaned_data.get("password")

        user_password = UserDetails.objects.get(id=self.cleaned_data.get("user_id")).user_password

        if not hashers.check_password(password,user_password):

            self.add_error("password","Incorrect password")


        return password

    def clean(self):

        cleaned_data = super().clean()

        pass1 = cleaned_data.get("new_password")
        pass2 = cleaned_data.get("conform_password")

        if pass1 and pass2 and pass1 != pass2:
            self.add_error("conformation_password", "Both passwords should be the same")


        return cleaned_data










