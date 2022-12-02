from django import forms
from django.forms import ModelForm
from .models import Book, Rate


class BookForm(ModelForm):
    class Meta:
        model = Book
        fields = [
            'name',
            'web',
            'price',
            'picture',
        ]


class ReviewForm(ModelForm):
    class Meta:
        model = Rate
        fields = ['rating']