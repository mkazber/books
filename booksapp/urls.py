from django.urls import path, include
from rest_framework import routers
from .views import BookViewSet, BookTypeViewSet

router = routers.DefaultRouter()
router.register('books', BookViewSet)
router.register('booktypes', BookTypeViewSet)

urlpatterns = [
    path('', include(router.urls))
]
