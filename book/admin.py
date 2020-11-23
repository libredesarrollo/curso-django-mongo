from django.contrib import admin

from .models import Book, Category, Tag
from .forms import BookForm
# Register your models here.

@admin.register(Book)
class AdminBook(admin.ModelAdmin):
    form = BookForm

@admin.register(Category)
class AdminCategory(admin.ModelAdmin):
    pass

@admin.register(Tag)
class TagCategory(admin.ModelAdmin):
    pass