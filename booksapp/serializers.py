# from rest_framework import serializers
# from django.contrib import admin
# from .models import Book, BookType, BookIsbn, Author, Rating, Publishing
#
# class BookTypeSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = BookType
#         fields = ['id', 'name']
#
# class BookIsbnSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = BookIsbn
#         fields = ['id', 'isbn_10', 'isbn_13']
#
# class AuthorSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Author
#         fields = ['id', 'name', 'surname']
#
# class PublishingSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Publishing
#         fields = ['id', 'name']
#
# class BookSerializer(serializers.ModelSerializer):
#     type = BookTypeSerializer(many=True)
#     isbn = BookIsbnSerializer(many=False)
#     authors = AuthorSerializer(many=True)
#     publishing = PublishingSerializer(many=False)
#     class Meta:
#         model = Book
#         fields = ['id','title','authors','type','publishing','isbn','numberOfPages', 'releaseDate', 'desc','cover','slug']
#
# class BookMiniSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Book
#         fields = ['id','title']
#
# class RatingSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Rating
#         fields = ['id']