from rest_framework import viewsets
from .models import Book, Author, Tag, ReadingLog
from .serializers import BookSerializer, AuthorSerializer, TagSerializer, 

class AuthorViewSet(viewsets.ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer

class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer

class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.select_related('author').prefetch_related('tags').all()
    serializer_class = BookSerializer