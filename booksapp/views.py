from django.contrib import messages
from rest_framework import viewsets
from .serializers import *
from .models import Book, BookType, Author, Publishing, BookIsbn, Rating, Profile
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.contrib.auth.decorators import login_required
from django.views.generic import View
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction
from .forms import UserForm, ProfileForm, BookForm, ProfileBooks, ContactForm, ForgotPassForm
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User
import random
import string
from random import sample

def randomString(stringLength=10):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(stringLength))

def returnBookRatings(q):
    r = Rating.objects.all()

    bookRatings = 0
    ratingsNumber = 0

    for rating in r:
        if rating.book == q:
            bookRatings += rating.rate
            ratingsNumber += 1

    if bookRatings > 0:
        bookRatings = bookRatings / ratingsNumber
    else:
        bookRatings = 0
    return bookRatings

class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

class BookTypeViewSet(viewsets.ModelViewSet):
    queryset = BookType.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

class AuthorViewSet(viewsets.ModelViewSet):
    queryset = Author.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

class PublishingViewSet(viewsets.ModelViewSet):
    queryset = Publishing.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

class BookIsbnViewSet(viewsets.ModelViewSet):
    queryset = BookIsbn.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

class RatingViewSet(viewsets.ModelViewSet):
    queryset = Rating.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

def mainPage(request):
    count = Book.objects.all().count()
    rand_ids = sample(range(1, count), 3)
    books3 = Book.objects.filter(id__in=rand_ids)

    rand_ids2 = sample(range(1, count), 1)
    booke1 = Book.objects.filter(id__in=rand_ids2)

    rand_ids3 = sample(range(1, count), 1)
    booke2 = Book.objects.filter(id__in=rand_ids3)

    return render(request, 'page/main.html', {'books3': books3, 'booke1': booke1, 'booke2': booke2})

def catalogPage(request):
    books = Book.objects.all()
    bookTypes = BookType.objects.all()
    publishings = Publishing.objects.all()
    authors = Author.objects.all()
    ratings = Rating.objects.all()
    if(request.method == "GET"):
        resultBookTypes = []
        resultPublishings = []
        resultAuthors = []
        resultBooks = []

        for bookType in bookTypes:
            FilterBookTypeID = "bookType" + str(bookType.id)
            if request.GET.get(FilterBookTypeID):
                resultBookTypes.insert(bookType.id, bookType)
        for publishing in publishings:
            filterPublishingID = "publishing" + str(publishing.id)
            if request.GET.get(filterPublishingID):
                resultPublishings.insert(publishing.id, publishing)
        for author in authors:
            filterAuthorID = "author" + str(author.id)
            if request.GET.get(filterAuthorID):
                resultAuthors.insert(author.id, author)

        i = 0
        for book in books:
            for bookType in book.types.all():
                for resultBookType in resultBookTypes:
                    if bookType == resultBookType:
                        if book not in resultBooks:
                            resultBooks.insert(i, book)
                            i1 = i+1
            for author in book.authors.all():
                for resultAuthor in resultAuthors:
                    if author == resultAuthor:
                        if book not in resultBooks:
                            resultBooks.insert(i, book)
                            i = i+1
            for resultPublishing in resultPublishings:
                if book.publishing == resultPublishing:
                    if book not in resultBooks:
                        resultBooks.insert(i, book)
                        i = i+1
        if resultBooks:
            books = resultBooks

    context = {
        'books': books,
        'bookTypes': bookTypes,
        'publishings': publishings,
        'authors': authors,
        'ratings': ratings,
    }
    return render(request, 'page/catalog.html', context)

# Sortowanie
def catalogRateAsc(request):  #rosnąco
    bookTypes = BookType.objects.all()
    publishings = Publishing.objects.all()
    authors = Author.objects.all()
    ratings = Rating.objects.all()

    books = Book.objects.order_by('averageRate')
    books = books.reverse()

    context = {
        'books': books,
        'bookTypes': bookTypes,
        'publishings': publishings,
        'authors': authors,
        'ratings': ratings,
    }
    return render(request, 'page/catalog.html', context)

def catalogRateDesc(request):  #malejąco
    bookTypes = BookType.objects.all()
    publishings = Publishing.objects.all()
    authors = Author.objects.all()
    ratings = Rating.objects.all()

    books = Book.objects.order_by('averageRate')
    context = {
        'books': books,
        'bookTypes': bookTypes,
        'publishings': publishings,
        'authors': authors,
        'ratings': ratings,
    }
    return render(request, 'page/catalog.html', context)

def catalogTitleAsc(request):  #rosnąco
    bookTypes = BookType.objects.all()
    publishings = Publishing.objects.all()
    authors = Author.objects.all()
    ratings = Rating.objects.all()

    books = Book.objects.order_by('title')
    books = books.reverse()

    context = {
        'books': books,
        'bookTypes': bookTypes,
        'publishings': publishings,
        'authors': authors,
        'ratings': ratings,
    }
    return render(request, 'page/catalog.html', context)

def catalogTitleDesc(request):  #malejąco
    bookTypes = BookType.objects.all()
    publishings = Publishing.objects.all()
    authors = Author.objects.all()
    ratings = Rating.objects.all()

    books = Book.objects.order_by('title')
    context = {
        'books': books,
        'bookTypes': bookTypes,
        'publishings': publishings,
        'authors': authors,
        'ratings': ratings,
    }
    return render(request, 'page/catalog.html', context)

def catalogAuthorAsc(request):  #rosnąco
    bookTypes = BookType.objects.all()
    publishings = Publishing.objects.all()
    authors = Author.objects.all()
    ratings = Rating.objects.all()

    books = Book.objects.order_by('authors')
    books = books.reverse()

    context = {
        'books': books,
        'bookTypes': bookTypes,
        'publishings': publishings,
        'authors': authors,
        'ratings': ratings,
    }
    return render(request, 'page/catalog.html', context)

def catalogAuthorDesc(request):  #malejąco
    bookTypes = BookType.objects.all()
    publishings = Publishing.objects.all()
    authors = Author.objects.all()
    ratings = Rating.objects.all()

    books = Book.objects.order_by('authors')
    context = {
        'books': books,
        'bookTypes': bookTypes,
        'publishings': publishings,
        'authors': authors,
        'ratings': ratings,
    }
    return render(request, 'page/catalog.html', context)

def catalogReadAsc(request):  #rosnąco
    bookTypes = BookType.objects.all()
    publishings = Publishing.objects.all()
    authors = Author.objects.all()
    ratings = Rating.objects.all()

    books = Book.objects.order_by('read')
    books = books.reverse()

    context = {
        'books': books,
        'bookTypes': bookTypes,
        'publishings': publishings,
        'authors': authors,
        'ratings': ratings,
    }
    return render(request, 'page/catalog.html', context)

def catalogReadDesc(request):  #malejąco
    bookTypes = BookType.objects.all()
    publishings = Publishing.objects.all()
    authors = Author.objects.all()
    ratings = Rating.objects.all()

    books = Book.objects.order_by('read')
    context = {
        'books': books,
        'bookTypes': bookTypes,
        'publishings': publishings,
        'authors': authors,
        'ratings': ratings,
    }
    return render(request, 'page/catalog.html', context)
# Koniec sortowania
def authorPage(request):
    authors = Author.objects.all()

    context = {
        'authors': authors,
    }

    return render(request, 'page/author.html', context)

def publishingPage(request):
    publishings = Publishing.objects.all()

    context = {
        'publishings': publishings,
    }

    return render(request, 'page/publishing.html', context)

def booktypesPage(request):
    bookTypes = BookType.objects.all()

    context = {
        'bookTypes': bookTypes,
    }

    return render(request, 'page/bookType.html', context)

def singleBook(request, slug_text):
    q = Book.objects.filter(slug=slug_text)
    r = Rating.objects.all()

    if q.exists():
        q = q.first()
    else:
        return HttpResponse("<h1>Page Not Found</h1>")

    ratingOfBooks = Rating.objects.filter(book=q)

    bookRatings = 0
    ratingsNumber = 0
    rating1 = 0
    rating2 = 0
    rating3 = 0
    rating4 = 0
    rating5 = 0
    for rating in r:
        if rating.book == q:
            bookRatings += rating.rate
            ratingsNumber += 1
            if rating.rate == 1:
                rating1 += 1
            if rating.rate == 2:
                rating2 += 1
            if rating.rate == 3:
                rating3 += 1
            if rating.rate == 4:
                rating4 += 1
            if rating.rate == 5:
                rating5 += 1
    if bookRatings > 0:
        bookRatings = bookRatings / ratingsNumber
    else:
        bookRatigns = 0
    if ratingsNumber > 0:
        rating1nr = int((rating1 / ratingsNumber)*100)
        rating2nr = int((rating2 / ratingsNumber)*100)
        rating3nr = int((rating3 / ratingsNumber)*100)
        rating4nr = int((rating4 / ratingsNumber)*100)
        rating5nr = int((rating5 / ratingsNumber)*100)
    else:
        rating1nr = 0
        rating2nr = 0
        rating3nr = 0
        rating4nr = 0
        rating5nr = 0

    context = {
        'book': q,
        'bookRatings': bookRatings,
        'ratingOfBooks': ratingOfBooks,
        'rating1': rating1,
        'rating1nr': rating1nr,
        'rating2': rating2,
        'rating2nr': rating2nr,
        'rating3': rating3,
        'rating3nr': rating3nr,
        'rating4': rating4,
        'rating4nr': rating4nr,
        'rating5': rating5,
        'rating5nr': rating5nr,
    }
    return render(request, 'page/book.html', context)

def singleAuthor(request, slug_text):
    author = Author.objects.filter(slug=slug_text)

    if author.exists():
        author = author.first()
    else:
        return HttpResponse("<h1>Page Not Found</h1>")

    books = Book.objects.all().filter(authors__slug=slug_text)
    profilesRead = Profile.objects.all().filter(readBooks__authors=author).count()
    profilesWantRead = Profile.objects.all().filter(booksToRead__authors=author).count()

    averageRate = 0
    number = 0
    for book in books:
        averageRate += book.averageRate
        number += 1
    if number:
        averageRate /= number
    else:
        averageRate = 0

    context = {
        'author': author,
        'books': books,
        'averageRate': averageRate,
        'profilesRead': profilesRead,
        'profilesWantRead': profilesWantRead,
    }

    return render(request, 'page/oneAuthor.html', context)


# Sortowanie
def singleAuthorRateAsc(request, slug_text):  # rosnąco
    author = Author.objects.filter(slug=slug_text)

    if author.exists():
        author = author.first()
    else:
        return HttpResponse("<h1>Page Not Found</h1>")

    books = Book.objects.all().filter(authors__slug=slug_text).order_by('averageRate')
    books = books.reverse()
    profilesRead = Profile.objects.all().filter(readBooks__authors=author).count()
    profilesWantRead = Profile.objects.all().filter(booksToRead__authors=author).count()

    averageRate = 0
    number = 0
    for book in books:
        averageRate += book.averageRate
        number += 1
    if number:
        averageRate /= number
    else:
        averageRate = 0

    context = {
        'author': author,
        'books': books,
        'averageRate': averageRate,
        'profilesRead': profilesRead,
        'profilesWantRead': profilesWantRead,
    }

    return render(request, 'page/oneAuthor.html', context)

def singleAuthorRateDesc(request, slug_text):  # malejąco
    author = Author.objects.filter(slug=slug_text)

    if author.exists():
        author = author.first()
    else:
        return HttpResponse("<h1>Page Not Found</h1>")

    books = Book.objects.all().filter(authors__slug=slug_text).order_by('averageRate')
    profilesRead = Profile.objects.all().filter(readBooks__authors=author).count()
    profilesWantRead = Profile.objects.all().filter(booksToRead__authors=author).count()

    averageRate = 0
    number = 0
    for book in books:
        averageRate += book.averageRate
        number += 1
    if number:
        averageRate /= number
    else:
        averageRate = 0

    context = {
        'author': author,
        'books': books,
        'averageRate': averageRate,
        'profilesRead': profilesRead,
        'profilesWantRead': profilesWantRead,
    }

    return render(request, 'page/oneAuthor.html', context)

def singleAuthorTitleAsc(request, slug_text):  # rosnąco
    author = Author.objects.filter(slug=slug_text)

    if author.exists():
        author = author.first()
    else:
        return HttpResponse("<h1>Page Not Found</h1>")

    books = Book.objects.all().filter(authors__slug=slug_text).order_by('title')
    books = books.reverse()
    profilesRead = Profile.objects.all().filter(readBooks__authors=author).count()
    profilesWantRead = Profile.objects.all().filter(booksToRead__authors=author).count()

    averageRate = 0
    number = 0
    for book in books:
        averageRate += book.averageRate
        number += 1
    if number:
        averageRate /= number
    else:
        averageRate = 0

    context = {
        'author': author,
        'books': books,
        'averageRate': averageRate,
        'profilesRead': profilesRead,
        'profilesWantRead': profilesWantRead,
    }

    return render(request, 'page/oneAuthor.html', context)

def singleAuthorTitleDesc(request, slug_text):  # malejąco
    author = Author.objects.filter(slug=slug_text)

    if author.exists():
        author = author.first()
    else:
        return HttpResponse("<h1>Page Not Found</h1>")

    books = Book.objects.all().filter(authors__slug=slug_text).order_by('title')
    profilesRead = Profile.objects.all().filter(readBooks__authors=author).count()
    profilesWantRead = Profile.objects.all().filter(booksToRead__authors=author).count()

    averageRate = 0
    number = 0
    for book in books:
        averageRate += book.averageRate
        number += 1
    if number:
        averageRate /= number
    else:
        averageRate = 0

    context = {
        'author': author,
        'books': books,
        'averageRate': averageRate,
        'profilesRead': profilesRead,
        'profilesWantRead': profilesWantRead,
    }

    return render(request, 'page/oneAuthor.html', context)

def singleAuthorPublishingAsc(request, slug_text):  # rosnąco
    author = Author.objects.filter(slug=slug_text)

    if author.exists():
        author = author.first()
    else:
        return HttpResponse("<h1>Page Not Found</h1>")

    books = Book.objects.all().filter(authors__slug=slug_text).order_by('publishing')
    books = books.reverse()
    profilesRead = Profile.objects.all().filter(readBooks__authors=author).count()
    profilesWantRead = Profile.objects.all().filter(booksToRead__authors=author).count()

    averageRate = 0
    number = 0
    for book in books:
        averageRate += book.averageRate
        number += 1
    if number:
        averageRate /= number
    else:
        averageRate = 0

    context = {
        'author': author,
        'books': books,
        'averageRate': averageRate,
        'profilesRead': profilesRead,
        'profilesWantRead': profilesWantRead,
    }

    return render(request, 'page/oneAuthor.html', context)

def singleAuthorPublishingDesc(request, slug_text):  # malejąco
    author = Author.objects.filter(slug=slug_text)

    if author.exists():
        author = author.first()
    else:
        return HttpResponse("<h1>Page Not Found</h1>")

    books = Book.objects.all().filter(authors__slug=slug_text).order_by('publishing')
    profilesRead = Profile.objects.all().filter(readBooks__authors=author).count()
    profilesWantRead = Profile.objects.all().filter(booksToRead__authors=author).count()

    averageRate = 0
    number = 0
    for book in books:
        averageRate += book.averageRate
        number += 1
    if number:
        averageRate /= number
    else:
        averageRate = 0

    context = {
        'author': author,
        'books': books,
        'averageRate': averageRate,
        'profilesRead': profilesRead,
        'profilesWantRead': profilesWantRead,
    }

    return render(request, 'page/oneAuthor.html', context)

def singleAuthorReadAsc(request, slug_text):  # rosnąco
    author = Author.objects.filter(slug=slug_text)

    if author.exists():
        author = author.first()
    else:
        return HttpResponse("<h1>Page Not Found</h1>")

    books = Book.objects.all().filter(authors__slug=slug_text).order_by('read')
    books = books.reverse()
    profilesRead = Profile.objects.all().filter(readBooks__authors=author).count()
    profilesWantRead = Profile.objects.all().filter(booksToRead__authors=author).count()

    averageRate = 0
    number = 0
    for book in books:
        averageRate += book.averageRate
        number += 1
    if number:
        averageRate /= number
    else:
        averageRate = 0

    context = {
        'author': author,
        'books': books,
        'averageRate': averageRate,
        'profilesRead': profilesRead,
        'profilesWantRead': profilesWantRead,
    }

    return render(request, 'page/oneAuthor.html', context)

def singleAuthorReadDesc(request, slug_text):  # malejąco
    author = Author.objects.filter(slug=slug_text)

    if author.exists():
        author = author.first()
    else:
        return HttpResponse("<h1>Page Not Found</h1>")

    books = Book.objects.all().filter(authors__slug=slug_text).order_by('read')
    profilesRead = Profile.objects.all().filter(readBooks__authors=author).count()
    profilesWantRead = Profile.objects.all().filter(booksToRead__authors=author).count()

    averageRate = 0
    number = 0
    for book in books:
        averageRate += book.averageRate
        number += 1
    if number:
        averageRate /= number
    else:
        averageRate = 0

    context = {
        'author': author,
        'books': books,
        'averageRate': averageRate,
        'profilesRead': profilesRead,
        'profilesWantRead': profilesWantRead,
    }

    return render(request, 'page/oneAuthor.html', context)

# Koniec sortowania

def singlePublishing(request, slug_text):
    publishing = Publishing.objects.filter(slug=slug_text)

    if publishing.exists():
        publishing = publishing.first()
    else:
        return HttpResponse("<h1>Page Not Found</h1>")

    books = Book.objects.all().filter(publishing__slug=slug_text)
    profilesRead = Profile.objects.all().filter(readBooks__publishing=publishing).count()
    profilesWantRead = Profile.objects.all().filter(booksToRead__publishing=publishing).count()

    averageRate = 0
    number = 0
    for book in books:
        averageRate += book.averageRate
        number += 1
    if number:
        averageRate /= number
    else:
        averageRate = 0

    context = {
        'publishing': publishing,
        'books': books,
        'averageRate': averageRate,
        'profilesRead': profilesRead,
        'profilesWantRead': profilesWantRead,
    }

    return render(request, 'page/onePublishing.html', context)

# Sortowanie
def singlePublishingRateAsc(request, slug_text):  #rosnąco
    publishing = Publishing.objects.filter(slug=slug_text)

    if publishing.exists():
        publishing = publishing.first()
    else:
        return HttpResponse("<h1>Page Not Found</h1>")

    books = Book.objects.all().filter(publishing__slug=slug_text).order_by('averageRate')
    books = books.reverse()
    profilesRead = Profile.objects.all().filter(readBooks__publishing=publishing).count()
    profilesWantRead = Profile.objects.all().filter(booksToRead__publishing=publishing).count()

    averageRate = 0
    number = 0
    for book in books:
        averageRate += book.averageRate
        number += 1
    if number:
        averageRate /= number
    else:
        averageRate = 0

    context = {
        'publishing': publishing,
        'books': books,
        'averageRate': averageRate,
        'profilesRead': profilesRead,
        'profilesWantRead': profilesWantRead,
    }

    return render(request, 'page/onePublishing.html', context)

def singlePublishingRateDesc(request, slug_text):  #malejąco
    publishing = Publishing.objects.filter(slug=slug_text)

    if publishing.exists():
        publishing = publishing.first()
    else:
        return HttpResponse("<h1>Page Not Found</h1>")

    books = Book.objects.all().filter(publishing__slug=slug_text).order_by('averageRate')
    profilesRead = Profile.objects.all().filter(readBooks__publishing=publishing).count()
    profilesWantRead = Profile.objects.all().filter(booksToRead__publishing=publishing).count()

    averageRate = 0
    number = 0
    for book in books:
        averageRate += book.averageRate
        number += 1
    if number:
        averageRate /= number
    else:
        averageRate = 0

    context = {
        'publishing': publishing,
        'books': books,
        'averageRate': averageRate,
        'profilesRead': profilesRead,
        'profilesWantRead': profilesWantRead,
    }

    return render(request, 'page/onePublishing.html', context)

def singlePublishingTitleAsc(request, slug_text):  #rosnąco
    publishing = Publishing.objects.filter(slug=slug_text)

    if publishing.exists():
        publishing = publishing.first()
    else:
        return HttpResponse("<h1>Page Not Found</h1>")

    books = Book.objects.all().filter(publishing__slug=slug_text).order_by('title')
    books = books.reverse()
    profilesRead = Profile.objects.all().filter(readBooks__publishing=publishing).count()
    profilesWantRead = Profile.objects.all().filter(booksToRead__publishing=publishing).count()

    averageRate = 0
    number = 0
    for book in books:
        averageRate += book.averageRate
        number += 1
    if number:
        averageRate /= number
    else:
        averageRate = 0

    context = {
        'publishing': publishing,
        'books': books,
        'averageRate': averageRate,
        'profilesRead': profilesRead,
        'profilesWantRead': profilesWantRead,
    }

    return render(request, 'page/onePublishing.html', context)

def singlePublishingTitleDesc(request, slug_text):  #malejąco
    publishing = Publishing.objects.filter(slug=slug_text)

    if publishing.exists():
        publishing = publishing.first()
    else:
        return HttpResponse("<h1>Page Not Found</h1>")

    books = Book.objects.all().filter(publishing__slug=slug_text).order_by('title')

    profilesRead = Profile.objects.all().filter(readBooks__publishing=publishing).count()
    profilesWantRead = Profile.objects.all().filter(booksToRead__publishing=publishing).count()

    averageRate = 0
    number = 0
    for book in books:
        averageRate += book.averageRate
        number += 1
    if number:
        averageRate /= number
    else:
        averageRate = 0

    context = {
        'publishing': publishing,
        'books': books,
        'averageRate': averageRate,
        'profilesRead': profilesRead,
        'profilesWantRead': profilesWantRead,
    }

    return render(request, 'page/onePublishing.html', context)

def singlePublishingAuthorAsc(request, slug_text):  #rosnąco
    publishing = Publishing.objects.filter(slug=slug_text)

    if publishing.exists():
        publishing = publishing.first()
    else:
        return HttpResponse("<h1>Page Not Found</h1>")

    books = Book.objects.all().filter(publishing__slug=slug_text).order_by('authors')
    books = books.reverse()
    profilesRead = Profile.objects.all().filter(readBooks__publishing=publishing).count()
    profilesWantRead = Profile.objects.all().filter(booksToRead__publishing=publishing).count()

    averageRate = 0
    number = 0
    for book in books:
        averageRate += book.averageRate
        number += 1
    if number:
        averageRate /= number
    else:
        averageRate = 0

    context = {
        'publishing': publishing,
        'books': books,
        'averageRate': averageRate,
        'profilesRead': profilesRead,
        'profilesWantRead': profilesWantRead,
    }

    return render(request, 'page/onePublishing.html', context)

def singlePublishingAuthorDesc(request, slug_text):  #malejąco
    publishing = Publishing.objects.filter(slug=slug_text)

    if publishing.exists():
        publishing = publishing.first()
    else:
        return HttpResponse("<h1>Page Not Found</h1>")

    books = Book.objects.all().filter(publishing__slug=slug_text).order_by('authors')
    profilesRead = Profile.objects.all().filter(readBooks__publishing=publishing).count()
    profilesWantRead = Profile.objects.all().filter(booksToRead__publishing=publishing).count()

    averageRate = 0
    number = 0
    for book in books:
        averageRate += book.averageRate
        number += 1
    if number:
        averageRate /= number
    else:
        averageRate = 0

    context = {
        'publishing': publishing,
        'books': books,
        'averageRate': averageRate,
        'profilesRead': profilesRead,
        'profilesWantRead': profilesWantRead,
    }

    return render(request, 'page/onePublishing.html', context)

def singlePublishingReadAsc(request, slug_text):  #rosnąco
    publishing = Publishing.objects.filter(slug=slug_text)

    if publishing.exists():
        publishing = publishing.first()
    else:
        return HttpResponse("<h1>Page Not Found</h1>")

    books = Book.objects.all().filter(publishing__slug=slug_text).order_by('read')
    books = books.reverse()
    profilesRead = Profile.objects.all().filter(readBooks__publishing=publishing).count()
    profilesWantRead = Profile.objects.all().filter(booksToRead__publishing=publishing).count()

    averageRate = 0
    number = 0
    for book in books:
        averageRate += book.averageRate
        number += 1
    if number:
        averageRate /= number
    else:
        averageRate = 0

    context = {
        'publishing': publishing,
        'books': books,
        'averageRate': averageRate,
        'profilesRead': profilesRead,
        'profilesWantRead': profilesWantRead,
    }

    return render(request, 'page/onePublishing.html', context)

def singlePublishingReadDesc(request, slug_text):  #malejąco
    publishing = Publishing.objects.filter(slug=slug_text)

    if publishing.exists():
        publishing = publishing.first()
    else:
        return HttpResponse("<h1>Page Not Found</h1>")

    books = Book.objects.all().filter(publishing__slug=slug_text).order_by('read')
    profilesRead = Profile.objects.all().filter(readBooks__publishing=publishing).count()
    profilesWantRead = Profile.objects.all().filter(booksToRead__publishing=publishing).count()

    averageRate = 0
    number = 0
    for book in books:
        averageRate += book.averageRate
        number += 1
    if number:
        averageRate /= number
    else:
        averageRate = 0

    context = {
        'publishing': publishing,
        'books': books,
        'averageRate': averageRate,
        'profilesRead': profilesRead,
        'profilesWantRead': profilesWantRead,
    }

    return render(request, 'page/onePublishing.html', context)
# Koniec sortowania

def singleBookType(request, slug_text):
    bookType = BookType.objects.filter(slug=slug_text)

    if bookType.exists():
        bookType = bookType.first()
    else:
        return HttpResponse("<h1>Page Not Found</h1>")

    books = Book.objects.all().filter(types__name=bookType)
    profilesRead = Profile.objects.all().filter(readBooks__types=bookType).count()
    profilesWantRead = Profile.objects.all().filter(booksToRead__types=bookType).count()

    averageRate = 0
    number = 0
    for book in books:
        averageRate += book.averageRate
        number +=1
    if number:
        averageRate /= number
    else:
        averageRate = 0

    context = {
        'bookType': bookType,
        'books': books,
        'averageRate': averageRate,
        'profilesRead': profilesRead,
        'profilesWantRead': profilesWantRead,
    }

    return render(request, 'page/oneType.html', context)

# Sortowanie
def singleBookTypeRateAsc(request, slug_text):  #rosnąco
    bookType = BookType.objects.filter(slug=slug_text)

    if bookType.exists():
        bookType = bookType.first()
    else:
        return HttpResponse("<h1>Page Not Found</h1>")

    books = Book.objects.all().filter(types__name=bookType).order_by('averageRate')
    books = books.reverse()
    profilesRead = Profile.objects.all().filter(readBooks__types=bookType).count()
    profilesWantRead = Profile.objects.all().filter(booksToRead__types=bookType).count()

    averageRate = 0
    number = 0
    for book in books:
        averageRate += book.averageRate
        number += 1
    if number:
        averageRate /= number
    else:
        averageRate = 0

    context = {
        'bookType': bookType,
        'books': books,
        'averageRate': averageRate,
        'profilesRead': profilesRead,
        'profilesWantRead': profilesWantRead,
    }

    return render(request, 'page/oneType.html', context)

def singleBookTypeRateDesc(request, slug_text):  #malejąco
    bookType = BookType.objects.filter(slug=slug_text)

    if bookType.exists():
        bookType = bookType.first()
    else:
        return HttpResponse("<h1>Page Not Found</h1>")

    books = Book.objects.all().filter(types__name=bookType).order_by('averageRate')
    profilesRead = Profile.objects.all().filter(readBooks__types=bookType).count()
    profilesWantRead = Profile.objects.all().filter(booksToRead__types=bookType).count()

    averageRate = 0
    number = 0
    for book in books:
        averageRate += book.averageRate
        number += 1
    if number:
        averageRate /= number
    else:
        averageRate = 0

    context = {
        'bookType': bookType,
        'books': books,
        'averageRate': averageRate,
        'profilesRead': profilesRead,
        'profilesWantRead': profilesWantRead,
    }

    return render(request, 'page/oneType.html', context)

def singleBookTypeTitleAsc(request, slug_text):  #rosnąco
    bookType = BookType.objects.filter(slug=slug_text)

    if bookType.exists():
        bookType = bookType.first()
    else:
        return HttpResponse("<h1>Page Not Found</h1>")

    books = Book.objects.all().filter(types__name=bookType).order_by('title')
    books = books.reverse()
    profilesRead = Profile.objects.all().filter(readBooks__types=bookType).count()
    profilesWantRead = Profile.objects.all().filter(booksToRead__types=bookType).count()

    averageRate = 0
    number = 0
    for book in books:
        averageRate += book.averageRate
        number += 1
    if number:
        averageRate /= number
    else:
        averageRate = 0

    context = {
        'bookType': bookType,
        'books': books,
        'averageRate': averageRate,
        'profilesRead': profilesRead,
        'profilesWantRead': profilesWantRead,
    }

    return render(request, 'page/oneType.html', context)

def singleBookTypeTitleDesc(request, slug_text):  #malejąco
    bookType = BookType.objects.filter(slug=slug_text)

    if bookType.exists():
        bookType = bookType.first()
    else:
        return HttpResponse("<h1>Page Not Found</h1>")

    books = Book.objects.all().filter(types__name=bookType).order_by('title')

    profilesRead = Profile.objects.all().filter(readBooks__types=bookType).count()
    profilesWantRead = Profile.objects.all().filter(booksToRead__types=bookType).count()

    averageRate = 0
    number = 0
    for book in books:
        averageRate += book.averageRate
        number += 1
    if number:
        averageRate /= number
    else:
        averageRate = 0

    context = {
        'bookType': bookType,
        'books': books,
        'averageRate': averageRate,
        'profilesRead': profilesRead,
        'profilesWantRead': profilesWantRead,
    }

    return render(request, 'page/oneType.html', context)

def singleBookTypeAuthorAsc(request, slug_text):  #rosnąco
    bookType = BookType.objects.filter(slug=slug_text)

    if bookType.exists():
        bookType = bookType.first()
    else:
        return HttpResponse("<h1>Page Not Found</h1>")

    books = Book.objects.all().filter(types__name=bookType).order_by('authors')
    books = books.reverse()
    profilesRead = Profile.objects.all().filter(readBooks__types=bookType).count()
    profilesWantRead = Profile.objects.all().filter(booksToRead__types=bookType).count()

    averageRate = 0
    number = 0
    for book in books:
        averageRate += book.averageRate
        number += 1
    if number:
        averageRate /= number
    else:
        averageRate = 0

    context = {
        'bookType': bookType,
        'books': books,
        'averageRate': averageRate,
        'profilesRead': profilesRead,
        'profilesWantRead': profilesWantRead,
    }

    return render(request, 'page/oneType.html', context)

def singleBookTypeAuthorDesc(request, slug_text):  #malejąco
    bookType = BookType.objects.filter(slug=slug_text)

    if bookType.exists():
        bookType = bookType.first()
    else:
        return HttpResponse("<h1>Page Not Found</h1>")

    books = Book.objects.all().filter(types__name=bookType).order_by('authors')

    profilesRead = Profile.objects.all().filter(readBooks__types=bookType).count()
    profilesWantRead = Profile.objects.all().filter(booksToRead__types=bookType).count()

    averageRate = 0
    number = 0
    for book in books:
        averageRate += book.averageRate
        number += 1
    if number:
        averageRate /= number
    else:
        averageRate = 0

    context = {
        'bookType': bookType,
        'books': books,
        'averageRate': averageRate,
        'profilesRead': profilesRead,
        'profilesWantRead': profilesWantRead,
    }

    return render(request, 'page/oneType.html', context)

def singleBookTypeReadAsc(request, slug_text):  #rosnąco
    bookType = BookType.objects.filter(slug=slug_text)

    if bookType.exists():
        bookType = bookType.first()
    else:
        return HttpResponse("<h1>Page Not Found</h1>")

    books = Book.objects.all().filter(types__name=bookType).order_by('read')
    books = books.reverse()
    profilesRead = Profile.objects.all().filter(readBooks__types=bookType).count()
    profilesWantRead = Profile.objects.all().filter(booksToRead__types=bookType).count()

    averageRate = 0
    number = 0
    for book in books:
        averageRate += book.averageRate
        number += 1
    if number:
        averageRate /= number
    else:
        averageRate = 0

    context = {
        'bookType': bookType,
        'books': books,
        'averageRate': averageRate,
        'profilesRead': profilesRead,
        'profilesWantRead': profilesWantRead,
    }

    return render(request, 'page/oneType.html', context)

def singleBookTypeReadDesc(request, slug_text):  #malejąco
    bookType = BookType.objects.filter(slug=slug_text)

    if bookType.exists():
        bookType = bookType.first()
    else:
        return HttpResponse("<h1>Page Not Found</h1>")

    books = Book.objects.all().filter(types__name=bookType).order_by('read')

    profilesRead = Profile.objects.all().filter(readBooks__types=bookType).count()
    profilesWantRead = Profile.objects.all().filter(booksToRead__types=bookType).count()

    averageRate = 0
    number = 0
    for book in books:
        averageRate += book.averageRate
        number += 1
    if number:
        averageRate /= number
    else:
        averageRate = 0

    context = {
        'bookType': bookType,
        'books': books,
        'averageRate': averageRate,
        'profilesRead': profilesRead,
        'profilesWantRead': profilesWantRead,
    }

    return render(request, 'page/oneType.html', context)
# Koniec sortowania



def contactPage(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            admin_address = "ADMIN_ADRES_TX"
            responder_address = "RESPONDER_ADRES"
            client_address = request.POST['email']
            message_for_admin = """
                imię użytkownika: %s;
                adres użytkownika: %s
                treść zapytania:
                    %s
            """ % (request.POST['name'], client_address, request.POST['message'])
            message_for_client = """
                Witam,
                Dziękuję za wysłanie wiadomości.
                Udzielę odpowiedzi najszybciej jak to możliwe.
                Z Poważaniem,
                Admin Books
                ---
                Wiadomość została wygenerowana automatycznie. Proszę nie odpowiadać na tego maila.
            """
            try:
                """
                    EMAIL_HOST = "poczta.interia.pl"
                    EMAIL_HOST_USER = "USER_ADRES_RES"
                    EMAIL_HOST_PASSWORD = "PASS"
                    EMAIL_PORT = 465
                    EMAIL_USE_TLS = True
                """

                send_mail(request.POST['subject'], message_for_admin, responder_address, [admin_address,])
                send_mail(request.POST['subject'], message_for_client, responder_address, [client_address,])
            except BadHeaderError:
                print("Nie poprawny nagłówek")
            return redirect('contact')
    else:
        form = ContactForm()
    return render(request, 'page/contact.html', {'form':form })


def top10Page(request):
    books = Book.objects.order_by('averageRate')
    top10 = books.reverse()[:10]
    return render(request, 'page/top10.html', {'books': top10})

def readPage(request):
    books = request.user.profile.readBooks.all()

    context = {
        'books': books,
    }
    return render(request, 'page/read.html', context)

# Sortowanie
def readRateAsc(request):  #rosnąco
    books = request.user.profile.readBooks.order_by('averageRate')
    books = books.reverse()

    context = {
        'books': books,
    }
    return render(request, 'page/read.html', context)

def readRateDesc(request):  #malejąco
    books = request.user.profile.readBooks.order_by('averageRate')
    context = {
        'books': books,
    }
    return render(request, 'page/read.html', context)

def readTitleAsc(request):  #rosnąco
    books = request.user.profile.readBooks.order_by('title')
    books = books.reverse()

    context = {
        'books': books,
    }
    return render(request, 'page/read.html', context)

def readTitleDesc(request):  #malejąco
    books = request.user.profile.readBooks.order_by('title')

    context = {
        'books': books,
    }
    return render(request, 'page/read.html', context)

def readAuthorAsc(request):  #rosnąco
    books = request.user.profile.readBooks.order_by('authors')
    books = books.reverse()

    context = {
        'books': books,
    }
    return render(request, 'page/read.html', context)

def readAuthorDesc(request):  #malejąco
    books = request.user.profile.readBooks.order_by('authors')

    context = {
        'books': books,
    }
    return render(request, 'page/read.html', context)

def readReadAsc(request):  #rosnąco
    books = request.user.profile.readBooks.order_by('read')
    books = books.reverse()

    context = {
        'books': books,
    }
    return render(request, 'page/read.html', context)

def readReadDesc(request):  #malejąco
    books = request.user.profile.readBooks.order_by('read')

    context = {
        'books': books,
    }
    return render(request, 'page/read.html', context)
# Koniec sortowania

def notreadPage(request):
    return render(request, 'page/notRead.html')
# Sortowanie
def notreadRateAsc(request):  #rosnąco
    books = request.user.profile.booksToRead.order_by('averageRate')
    books = books.reverse()

    context = {
        'books': books,
    }
    return render(request, 'page/notRead.html', context)

def notreadRateDesc(request):  #malejąco
    books = request.user.profile.booksToRead.order_by('averageRate')
    context = {
        'books': books,
    }
    return render(request, 'page/notRead.html', context)

def notreadTitleAsc(request):  #rosnąco
    books = request.user.profile.booksToRead.order_by('title')
    books = books.reverse()

    context = {
        'books': books,
    }
    return render(request, 'page/notRead.html', context)

def notreadTitleDesc(request):  #malejąco
    books = request.user.profile.booksToRead.order_by('title')

    context = {
        'books': books,
    }
    return render(request, 'page/notRead.html', context)

def notreadAuthorAsc(request):  #rosnąco
    books = request.user.profile.booksToRead.order_by('authors')
    books = books.reverse()

    context = {
        'books': books,
    }
    return render(request, 'page/notRead.html', context)

def notreadAuthorDesc(request):  #malejąco
    books = request.user.profile.booksToRead.order_by('authors')

    context = {
        'books': books,
    }
    return render(request, 'page/notRead.html', context)

def notreadReadAsc(request):  #rosnąco
    books = request.user.profile.booksToRead.order_by('read')
    books = books.reverse()

    context = {
        'books': books,
    }
    return render(request, 'page/notRead.html', context)

def notreadReadDesc(request):  #malejąco
    books = request.user.profile.booksToRead.order_by('read')

    context = {
        'books': books,
    }
    return render(request, 'page/notRead.html', context)
# Koniec sortowania

def registerPage(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            # log the user in
            return redirect(mainPage)
    else:
        form = UserCreationForm()
    return render(request, 'page/register.html', { 'form':form })

def forgotpassPage(request):
    if request.method == "POST":
        form = ForgotPassForm(request.POST)
        if form.is_valid():
            admin_address = "ADMIN"
            responder_address = "RESPONDER_ADDRES"
            client_address = request.POST['email']

            user = User.objects.all().filter(email=request.POST['email'])
            if user.exists():
                user = user.first()
            else:
                return HttpResponse("<h1>Nie ma takiego użytkownika</h1>")
            randstr = randomString()
            user.set_password(randstr)
            user.save()

            message_for_admin = """
                adres użytkownika: %s
                Czynność:
                    Przypomnienie hasła.
            """ % (client_address)
            message_for_client = """
                Witam,
                Twoje nowe hasło do serwisu Books znajduje się na dole wiadomości.
                Admin Books
                ---
                Wiadomość została wygenerowana automatycznie. Proszę nie odpowiadać na tego maila.
            """ + str(randstr) + " - Zmień hasło jak najszybciej na nowe."
            try:
                """
                    EMAIL_HOST = "poczta.interia.pl"
                    EMAIL_HOST_USER = "HOST_ADDRES"
                    EMAIL_HOST_PASSWORD = "PASS"
                    EMAIL_PORT = 465
                    EMAIL_USE_TLS = True
                """

                send_mail("Przypomnienie hasła", message_for_admin, responder_address, [admin_address,])
                send_mail("Przypomnienie hasła", message_for_client, responder_address, [client_address,])
            except BadHeaderError:
                print("Nie poprawny nagłówek")
            return redirect('forgotpass')
    else:
        form = ForgotPassForm()
    return render(request, 'page/forgotpass.html', { 'form': form })

@login_required
def userProfilePage(request):
    return render(request, 'page/myprofile.html')

@login_required
@transaction.atomic
def update_profile(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            userpass = request.user.password
            newpass = request.POST['password']
            user_form.save()
            profile_form.save()

            request.user.set_password(newpass)
            request.user.save()

            messages.success(request, ('Your profile was successfully updated!'))
            return redirect(update_profile)
        else:
            messages.error(request, ('Please correct the error below.'))
    else:
        user_form = UserForm(instance=request.user)
        profile_form = ProfileForm(instance=request.user.profile)
    return render(request, 'page/myprofile.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })

@login_required
@transaction.atomic
def dodaj_opinie(request, slug_text):
    q = Book.objects.filter(slug=slug_text)

    if q.exists():
        q = q.first()
    else:
        return HttpResponse("<h1>Page Not Found</h1>")
    if request.method == 'POST':
        form = BookForm(request.POST, initial={'book': q, 'user': request.user})
        # profilebooks_form = ProfileBooks(request.POST, instance=request.user.profile, initial={'readBooks': [request.user.profile.readBooks.all(), q]})
        if form.is_valid(): # and profilebooks_form.is_valid()
            request.user.profile.readBooks.add(q)
            request.user.profile.booksToRead.remove(q)

            form.save()
            # profilebooks_form.save()
            q.read += 1
            q.averageRate = returnBookRatings(q)
            q.save()
            messages.success(request, ('Your profile was successfully updated!'))
            return redirect(readPage)  # tu ustawić z powrotem na tę książke której wystawialiśmy opinie
        else:
            messages.error(request, ('Please correct the error below.'))
    else:
        form = BookForm(instance=q, initial={'book': q, 'user': request.user})
        # profilebooks_form = ProfileBooks(instance=request.user.profile, initial={'readBooks': [request.user.profile.readBooks.all(), q]})
    return render(request, 'page/book_form.html', {'form': form, 'book': q}) # 'profilebooks_form': profilebooks_form ,

def add_to_read(request, slug_text):
    q = Book.objects.filter(slug=slug_text)

    if q.exists():
        q = q.first()
    else:
        return HttpResponse("<h1>Page Not Found</h1>")
    # read = request.user.profile.readBooks.all()

    # czyJest = read.get(id = q.id)

    # print(read.get(id = q.id))
    # if(request.user.profile.):
    request.user.profile.booksToRead.add(q)
    # else:
    #     messages.error(request, ('Już chcesz przeczytać tę książkę!'))
    return redirect(notreadPage)

