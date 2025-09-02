from django.db import models


# Create your models here.

class Users(models.Model):


    name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)

    password = models.CharField(max_length=256)

    token = models.CharField(max_length=40)

    is_verified = models.BooleanField(default=False)

    created_at = models.DateField(auto_now_add=True)


    def __str__(self):

        return self.name


