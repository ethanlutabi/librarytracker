from django.shortcuts import render, get_object_or_404
from django.db.models import Avg
from .models import Book


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