from django.http import HttpResponse
from django.shortcuts import render,redirect,reverse


from .forms import ExpenseForm
from .models import Expense
from django.db.models import Sum

import datetime

# Create your views here.



def index(request):


    if request.method == "POST":
        expense_form = ExpenseForm(request.POST)

        if expense_form.is_valid():


            expense_form.save()




    expenses = Expense.objects.all().order_by("-pk")
    total_expenses = expenses.aggregate(Sum("amount"))

    #logic to calculate 365 days
    def calculate_365():

        last_year = datetime.date.today() - datetime.timedelta(days=365)

        year_data = Expense.objects.filter(date__gte=last_year)
        yearly_sum = year_data.aggregate(Sum("amount"))

        return yearly_sum

    yearly_sum = calculate_365()

    #logic to calculate 30 days

    def calculate_30():


        last_month = datetime.date.today() - datetime.timedelta(days=30)
        month_data = Expense.objects.filter(date__gte=last_month)

        monthly_sum = month_data.aggregate(Sum("amount"))

        return monthly_sum

    monthly_sum = calculate_30()


    # 7 days

    def calculate_7():
        last_week = datetime.date.today() - datetime.timedelta(days=7)
        week_data = Expense.objects.filter(date__gte=last_week)

        week_sum = week_data.aggregate(Sum("amount"))

        return week_sum
    week_sum  = calculate_7()

    # today

    def today():
        today =  datetime.date.today()

        today_data = Expense.objects.filter(date__gte=today)
        today_sum = today_data.aggregate(Sum("amount"))

        return today_sum

    today_sum = today()

    last_month = datetime.date.today() - datetime.timedelta(days=30)
    daily_sums = Expense.objects.filter(date__gte=last_month).values("date").order_by("-date").annotate(sum=Sum("amount"))

    categorical_sums = Expense.objects.filter().values("category").order_by("category").annotate(sum=Sum("amount"))

    expense_form = ExpenseForm()


    return render(request,"myapp/index.html",{"expense_form":expense_form,"expenses":expenses,"total_expenses":total_expenses,
                                                                "yearly_sum":yearly_sum,"monthly_sum":monthly_sum,"week_sum":week_sum,"today_sum":today_sum,
                                              "daily_sums":daily_sums,"categorical_sums":categorical_sums})

def edit(request,id):

    expense = Expense.objects.get(id=id)



    if request.method == "POST":

        expense_form = ExpenseForm(request.POST,instance=expense)

        if expense_form.is_valid():

            expense_form.save()

            return  redirect('myapp:index')



    else:
        expense_form = ExpenseForm(instance=expense)


    return render(request,"myapp/edit.html",{"expense_form":expense_form})

def delete(request,id):

    if request.method == "POST" and "delete" in request.POST:

        expense = Expense.objects.get(id=id)

        expense.delete()

        return redirect('myapp:index')

    return HttpResponse("Something went wrong")

