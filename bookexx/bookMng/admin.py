from django.contrib import admin

# Register your models here.

from .models import MainMenu, Rate
from .models import Book

admin.site.register(MainMenu)
admin.site.register(Book)
admin.site.register(Rate)