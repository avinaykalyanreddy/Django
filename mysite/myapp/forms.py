
from django.forms import ModelForm
from .models import Expense
class ExpenseForm(ModelForm):

    class Meta:

        model = Expense

        fields = ["name","amount","category"]


    def clean(self):

        cleaned_data = super().clean()

        if "name" in cleaned_data:

            cleaned_data["name"] = cleaned_data["name"].title()

        if "category" in cleaned_data:

            cleaned_data["category"] = cleaned_data["category"].title()


        return cleaned_data