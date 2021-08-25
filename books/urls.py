from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from rest_framework.authtoken.views import obtain_auth_token
from django.contrib.auth import views as auth_views
from django.urls import re_path
from booksapp.views import *

urlpatterns = [
    path('books/', include('booksapp.urls')),
    path('', mainPage, name="main"),
    path('catalog/', catalogPage, name="catalog"),

    path('catalog/rate_asc/', catalogRateAsc, name="catalogRateAsc"),
    path('catalog/rate_desc/', catalogRateDesc, name="catalogRateDesc"),
    path('catalog/title_asc/', catalogTitleAsc, name="catalogTitleAsc"),
    path('catalog/title_desc/', catalogTitleDesc, name="catalogTitleDesc"),
    path('catalog/author_asc/', catalogAuthorAsc, name="catalogAuthorAsc"),
    path('catalog/author_desc/', catalogAuthorDesc, name="catalogAuthorDesc"),
    path('catalog/read_asc/', catalogReadAsc, name="catalogReadAsc"),
    path('catalog/read_desc/', catalogReadDesc, name="catalogReadDesc"),
    path('read/rate_asc/', readRateAsc, name="readRateAsc"),
    path('read/rate_desc/', readRateDesc, name="readRateDesc"),
    path('read/title_asc/', readTitleAsc, name="readTitleAsc"),
    path('read/title_desc/', readTitleDesc, name="readTitleDesc"),
    path('read/author_asc/', readAuthorAsc, name="readAuthorAsc"),
    path('read/author_desc/', readAuthorDesc, name="readAuthorDesc"),
    path('read/read_asc/', readReadAsc, name="readReadAsc"),
    path('read/read_desc/', readReadDesc, name="readReadDesc"),

    path('notread/rate_asc/', notreadRateAsc, name="notreadRateAsc"),
    path('notread/rate_desc/', notreadRateDesc, name="notreadRateDesc"),
    path('notread/title_asc/', notreadTitleAsc, name="notreadTitleAsc"),
    path('notread/title_desc/', notreadTitleDesc, name="notreadTitleDesc"),
    path('notread/author_asc/', notreadAuthorAsc, name="notreadAuthorAsc"),
    path('notread/author_desc/', notreadAuthorDesc, name="notreadAuthorDesc"),
    path('notread/read_asc/', notreadReadAsc, name="notreadReadAsc"),
    path('notread/read_desc/', notreadReadDesc, name="notreadReadDesc"),

    path('author/', authorPage, name="author"),
    path('publishing/', publishingPage, name="publishing"),
    path('booktypes/', booktypesPage, name="booktypes"),
    path('contact/', contactPage, name="contact"),
    path('top10', top10Page, name="top10"),
    path('books/<slug:slug_text>', singleBook, name="singleBook"),

    path('authors/<slug:slug_text>', singleAuthor, name="singleAuthor"),
    path('publishings/<slug:slug_text>', singlePublishing, name="singlePublishing"),
    path('booktypes/<slug:slug_text>', singleBookType, name="singleBookType"),

    path('booktypes/<slug:slug_text>/rate_asc/', singleBookTypeRateAsc, name="singleBookTypeRateAsc"),
    path('booktypes/<slug:slug_text>/rate_desc/', singleBookTypeRateDesc, name="singleBookTypeRateDesc"),
    path('booktypes/<slug:slug_text>/title_asc/', singleBookTypeTitleAsc, name="singleBookTypeTitleAsc"),
    path('booktypes/<slug:slug_text>/title_desc/', singleBookTypeTitleDesc, name="singleBookTypeTitleDesc"),
    path('booktypes/<slug:slug_text>/author_asc/', singleBookTypeAuthorAsc, name="singleBookTypeAuthorAsc"),
    path('booktypes/<slug:slug_text>/author_desc/', singleBookTypeAuthorDesc, name="singleBookTypeAuthorDesc"),
    path('booktypes/<slug:slug_text>/read_asc/', singleBookTypeReadAsc, name="singleBookTypeReadAsc"),
    path('booktypes/<slug:slug_text>/read_desc/', singleBookTypeReadDesc, name="singleBookTypeReadDesc"),

    path('publishings/<slug:slug_text>/rate_asc/', singlePublishingRateAsc, name="singlePublishingRateAsc"),
    path('publishings/<slug:slug_text>/rate_desc/', singlePublishingRateDesc, name="singlePublishingRateDesc"),
    path('publishings/<slug:slug_text>/title_asc/', singlePublishingTitleAsc, name="singlePublishingTitleAsc"),
    path('publishings/<slug:slug_text>/title_desc/', singlePublishingTitleDesc, name="singlePublishingTitleDesc"),
    path('publishings/<slug:slug_text>/author_asc/', singlePublishingAuthorAsc, name="singlePublishingAuthorAsc"),
    path('publishings/<slug:slug_text>/author_desc/', singlePublishingAuthorDesc, name="singlePublishingAuthorDesc"),
    path('publishings/<slug:slug_text>/read_asc/', singlePublishingReadAsc, name="singlePublishingReadAsc"),
    path('publishings/<slug:slug_text>/read_desc/', singlePublishingReadDesc, name="singlePublishingReadDesc"),

    path('authors/<slug:slug_text>/rate_asc/', singleAuthorRateAsc, name="singleAuthorRateAsc"),
    path('authors/<slug:slug_text>/rate_desc/', singleAuthorRateDesc, name="singleAuthorRateDesc"),
    path('authors/<slug:slug_text>/title_asc/', singleAuthorTitleAsc, name="singleAuthorTitleAsc"),
    path('authors/<slug:slug_text>/title_desc/', singleAuthorTitleDesc, name="singleAuthorTitleDesc"),
    path('authors/<slug:slug_text>/publishing_asc/', singleAuthorPublishingAsc, name="singleAuthorPublishingAsc"),
    path('authors/<slug:slug_text>/publishing_desc/', singleAuthorPublishingDesc, name="singleAuthorPublishingDesc"),
    path('authors/<slug:slug_text>/read_asc/', singleAuthorReadAsc, name="singleAuthorReadAsc"),
    path('authors/<slug:slug_text>/read_desc/', singleAuthorReadDesc, name="singleAuthorReadDesc"),

    path('read/', readPage, name="read"),
    path('notread/', notreadPage, name="notread"),
    path('admin/', admin.site.urls),
    path('auth/', obtain_auth_token),
    path('login/', auth_views.LoginView.as_view(), name="login"),
    path('register/', registerPage, name="register"),
    path('forgotpass/', forgotpassPage, name="forgotpass"),
    path('user_profile/', update_profile, name="user_profile"),
    path('logout/', auth_views.LogoutView.as_view(), name="logout"),
    path('dodaj_opinie/<slug:slug_text>', dodaj_opinie, name="dodaj_opinie"),
    path('add_to_read/<slug:slug_text>', add_to_read, name="add_to_read"),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)