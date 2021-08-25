from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from .utils import unique_slug_generator, unique_slug_generator_author, unique_slug_generator_publishing
from datetime import datetime


class Author(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=40, null=False)
    surname = models.CharField(max_length=40, null=False, blank=False)
    slug = models.SlugField(max_length=250, null=True, blank=True)

    def __str__(self):
        return self.name + " " + self.surname
    class Meta:
        unique_together = (('name','surname'),)

class BookType(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=40, null=False, unique=True)
    slug = models.SlugField(max_length=250, null=True, blank=True)
    def __str__(self):
        return self.name

class Publishing(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=40, null=True, blank=False, unique=True)
    slug = models.SlugField(max_length=250, null=True, blank=True)
    def __str__(self):
        return self.name

class BookIsbn(models.Model):
    id = models.AutoField(primary_key=True)
    isbn_10 = models.CharField(max_length=10, blank=True)
    isbn_13 = models.CharField(max_length=13, blank=True)
    def __str__(self):
        return self.isbn_10 + "/ " + self.isbn_13

class Book(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100)
    authors = models.ManyToManyField(Author, null=False)
    types = models.ManyToManyField(BookType, null=False)
    publishing = models.ForeignKey(Publishing, null=True, blank=False, on_delete=models.CASCADE)
    isbn = models.OneToOneField(BookIsbn, null=True, blank=False, on_delete=models.CASCADE)
    numberOfPages = models.IntegerField(null=True, blank=False)
    releaseDate = models.DateField(null=False, blank=False)
    desc = models.TextField(max_length=3000)
    cover = models.ImageField(upload_to='books/', blank=False)
    read = models.PositiveIntegerField(null=True, blank=True, default=0)
    averageRate = models.DecimalField(decimal_places=2, max_digits=3, null=True, blank=True, default=0)
    slug = models.SlugField(max_length=250, null=True, blank=True)

    def __str__(self):
        return self.title

class Rating(models.Model):
    id = models.AutoField(primary_key=True)
    review = models.TextField(default="", blank=True, max_length=10000, null=True)
    rate = models.PositiveSmallIntegerField(default=5, validators=[MinValueValidator(1), MaxValueValidator(5)], null=True)
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE, related_name='user')
    date = models.DateTimeField(default=datetime.now, blank=True, null=True)
    book = models.ForeignKey(Book, null=True, blank=True, on_delete=models.CASCADE)
    class Meta:
        unique_together = (('book','user'),)
        index_together = (('book', 'user'),)
    def __str__(self):
        return "Ocena: " + str(self.rate)

def slug_generator(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)

def slug_generator_author(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator_author(instance)

def slug_generator_publishing(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator_publishing(instance)

pre_save.connect(slug_generator, sender=Book)
pre_save.connect(slug_generator_author, sender=Author)
pre_save.connect(slug_generator_publishing, sender=Publishing)
pre_save.connect(slug_generator_publishing, sender=BookType)

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=1000, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    avatar = models.ImageField(upload_to='users/avatars/', blank=True, default="users/avatars/dflt.jpg")
    readBooks = models.ManyToManyField(Book, null=True, related_name='user_read_books')
    booksToRead = models.ManyToManyField(Book, null=True, related_name='user_books_to_red')

    def __str__(self):
        return self.user.username

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.profile.save()
