from django.contrib import admin
from .models import Book, BookType, BookIsbn, Author, Rating, Publishing, Profile

@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ['id','name','surname']
    search_fields = ['name','surname']

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ['id','title','averageRate' ,'isbn','releaseDate'] #,'type','authors'
    list_filter = ['id','title','averageRate', 'isbn','releaseDate'] # ,'type','authors'
    search_fields = ['title','isbn','releaseDate'] # ,'type','authors'

@admin.register(BookType)
class BookTypeAdmin(admin.ModelAdmin):
    list_display = ['id','name']
    search_fields = ['name']

@admin.register(BookIsbn)
class BookIsbnAdmin(admin.ModelAdmin):
    list_display = ['id','isbn_10','isbn_13']
    search_fields = ['isbn_10','isbn_13']

@admin.register(Publishing)
class PublishingAdmin(admin.ModelAdmin):
    list_display = ['id','name']
    search_fields = ['name']

@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = ['id', 'book', 'rate', 'user','date']
    list_filter = ['rate']
    search_fields = ['rate']

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'birth_date']