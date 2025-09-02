from django.db import models
from users.models import Users
# Create your models here.

class Expense(models.Model):

    user = models.ForeignKey(Users,on_delete=models.CASCADE,default=1)

    name = models.CharField(max_length=100)
    amount = models.PositiveIntegerField()
    category = models.CharField(max_length=50)

    date = models.DateField(auto_now=True)

    def __str__(self):

        return self.name




