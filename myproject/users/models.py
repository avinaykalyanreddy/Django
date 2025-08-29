from django.db import models

# Create your models here.

class UserDetails(models.Model):

    user_name = models.CharField(max_length=50)
    user_password = models.CharField(max_length=128)

    user_email  = models.EmailField()


    def __str__(self):

        return f"{self.user_name}"

class UserProfilePic(models.Model):

    user = models.OneToOneField(UserDetails,on_delete=models.CASCADE,related_name="userprofilepic")

    image = models.TextField(default="https://res.cloudinary.com/jerrick/image/upload/d_642250b563292b35f27461a7.png,f_jpg,q_auto,w_720/67338e73953975001dd4b461.png")

    def __str__(self):

        return f"{self.user.user_name}"
