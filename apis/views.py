from django.shortcuts import render
from rest_framework.generics import ListAPIView

from apis.serializers import BookSerializer
from books.models import Book

class BookAPIView(ListAPIView):

    queryset = Book.objects.all()

    serializer_class = BookSerializer



