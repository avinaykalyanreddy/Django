from django.http import HttpResponse
from django.shortcuts import render,redirect,reverse
from .context_processors import user_info

from .forms import ExpenseForm
from .models import Expense
from django.db.models import Sum
from users.models import Users
import datetime

# Create your views here.

def home(request):

    if not request.session.get("user_id"):

        request.session["user_id"] = 1




    return redirect("myapp:index")

def index(request):
    user_id = request.session.get("user_id", 1)

    if request.method == "POST":
        expense_form = ExpenseForm(request.POST)

        if expense_form.is_valid():

            user_obj = Users.objects.filter(id=user_id).first()

            expense = expense_form.save(commit=False)

            expense.user = user_obj



            expense.save()





    expenses = Expense.objects.filter(user_id=user_id).order_by("-pk")
    total_expenses = expenses.aggregate(Sum("amount"))

    #logic to calculate 365 days
    def calculate_365():

        last_year = datetime.date.today() - datetime.timedelta(days=365)

        year_data = Expense.objects.filter(user_id=user_id,date__gte=last_year)
        yearly_sum = year_data.aggregate(Sum("amount"))

        return yearly_sum

    yearly_sum = calculate_365()

    #logic to calculate 30 days

    def calculate_30():


        last_month = datetime.date.today() - datetime.timedelta(days=30)
        month_data = Expense.objects.filter(user_id=user_id,date__gte=last_month)

        monthly_sum = month_data.aggregate(Sum("amount"))

        return monthly_sum

    monthly_sum = calculate_30()


    # 7 days

    def calculate_7():
        last_week = datetime.date.today() - datetime.timedelta(days=7)
        week_data = Expense.objects.filter(user_id=user_id,date__gte=last_week)

        week_sum = week_data.aggregate(Sum("amount"))

        return week_sum
    week_sum  = calculate_7()

    # today

    def today():
        today =  datetime.date.today()

        today_data = Expense.objects.filter(user_id=user_id,date__gte=today)
        today_sum = today_data.aggregate(Sum("amount"))

        return today_sum

    today_sum = today()

    last_month = datetime.date.today() - datetime.timedelta(days=30)
    daily_sums = Expense.objects.filter(user_id=user_id,date__gte=last_month).values("date").order_by("-date").annotate(sum=Sum("amount"))

    categorical_sums = Expense.objects.filter(user_id=user_id).values("category").order_by("category").annotate(sum=Sum("amount"))

    expense_form = ExpenseForm()


    return render(request,"myapp/index.html",{"expense_form":expense_form,"expenses":expenses,"total_expenses":total_expenses,
                                                                "yearly_sum":yearly_sum,"monthly_sum":monthly_sum,"week_sum":week_sum,"today_sum":today_sum,
                                              "daily_sums":daily_sums,"categorical_sums":categorical_sums})

def edit(request,id):

    user_id = request.session.get("user_id")
    expense = Expense.objects.filter(user_id=user_id,id=id).first()

    if not expense:

        return HttpResponse(f"violating the site rule, go back to <a href= { reverse('myapp:index') } >Home</a>")



    if request.method == "POST":

        expense_form = ExpenseForm(request.POST,instance=expense)

        if expense_form.is_valid():

            expense_form.save()

            return  redirect('myapp:index')



    else:
        expense_form = ExpenseForm(instance=expense)


    return render(request,"myapp/edit.html",{"expense_form":expense_form})

def delete(request,id):
    user_id = request.session.get("user_id")
    expense = Expense.objects.filter(user_id=user_id, id=id).first()


    if expense and  request.method == "POST" and "delete" in request.POST:


        expense.delete()

        return redirect('myapp:index')

    return HttpResponse(f"violating the site rule, go back to <a href= { reverse('myapp:index') } >Home</a>")

