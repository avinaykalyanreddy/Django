
from django import forms
from .models import  Users
class UserSignUp(forms.ModelForm):

    confirm_password = forms.CharField(max_length=256, label="Confirm Password",widget= forms.PasswordInput())
    password = forms.CharField(max_length=256, label="Password",widget= forms.PasswordInput())

    class Meta:

        model = Users

        fields = ["name","email","password"]


    def clean_email(self):

            email = self.cleaned_data.get("email")

            is_email_exist = Users.objects.filter(email=email).first()

            if is_email_exist:

                self.add_error("email","A user with this email already exists. Please try another email")

            return email

    def clean(self):

        cleaned_data = super().clean()

        pass1 = cleaned_data.get("password",None)
        pass2 = cleaned_data.get("confirm_password")


        if  pass1 != pass2:

            self.add_error("password","Your passwords don’t match. Please try again.")

        elif len(pass1) < 5:

            self.add_error("password","Password length must be at least 5 characters")


        return cleaned_data


class UserLogin(forms.Form):

    email = forms.EmailField()
    password = forms.CharField(widget= forms.PasswordInput())
