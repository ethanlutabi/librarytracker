from django.shortcuts import redirect, render, get_object_or_404
from django.db.models import Avg
from .models import Book
from .forms import BookForm
from rest_framework import viewsets
from .models import Book, Author, Tag
from .serializers import BookSerializer, AuthorSerializer, TagSerializer


# Create your views here.


def bool_list(request):
    books = Book.objects.select_related('author').prefetch_related('tags').annotate(
        avg_rating=Avg('reading_logs__rating')
    )
    return render(request, 'tracker/book_list.html', {'books': books})


def book_detail(request, book_id):
    book = get_object_or_404(
        Book.objects.select_related('author').prefetch_related('tags','reading_logs'),
        id = book_id
    )
    return render(request, 'tracker/book_detail.html', {'book': book})

def book_create(request):
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('book_list')
    else:
        form = BookForm()
    return render(request, 'tracker/book_form.html', {'form': form})



def book_edit(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    if request.method == 'POST':
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            form.save()
            return redirect('book_detail', book_id=book.id)
    else:
        form = BookForm(instance=book)
    return render(request, 'tracker/book_form.html', {'form': form})


def book_delete(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    if request.method == 'POST':
        book.delete()
        return redirect('book_list')
    return render(request, 'tracker/book_confirm_delete.html', {'book': book})




class AuthorViewSet(viewsets.ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer

class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer

class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all().select_related('author').prefetch_related('tags')
    serializer_class = BookSerializer