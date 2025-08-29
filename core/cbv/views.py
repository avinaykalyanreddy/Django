
from django.shortcuts import render,redirect,reverse
from django.views import View
from django.http import HttpResponse
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView
from cbv.models import Book
from django.urls import reverse_lazy



class HelloView(View):

    def get(self,request):

        context = {"name":"A Vinay Kalyan Reddy","age":20}

        return render(request,"post.html",context=context)

    def post(self,request):

        return HttpResponse(" <h1> Hello, this POST response</h1>")


class HomePage(TemplateView):

    template_name = "home.html"

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)

        context["name"] = "A Vinay Kalyan Reddy"
        context["clg"] = "DSATM"

        return context

class BookListView(ListView):

    model = Book

    template_name = "book_lst.html"

class BookDetailView(DetailView):

    model = Book
    template_name = "book_detail.html"

class BookCreateView(CreateView):

    model = Book
    fields = ["title","author"]

    template_name = "book_form.html"

    def get_success_url(self):

        return reverse("book_detail",kwargs={"pk":self.object.pk})


class BookUpdateView(UpdateView):

    model = Book

    fields = ["title","author"]

    template_name = "update.html"

    def get_success_url(self):

        return reverse("book_detail",kwargs={"pk":self.object.pk})


class BookDeleteView(DeleteView):

    model = Book

    template_name = "delete.html"

    success_url = reverse_lazy("book_lst")