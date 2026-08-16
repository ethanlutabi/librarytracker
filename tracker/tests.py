from django.test import TestCase
from django.urls import reverse
from .models import Author, Book


class BookListViewTest(TestCase):
    def setUp(self):
        self.author = Author.objects.create(name="Frank Herbert", bio="Sci-fi author")
        self.book = Book.objects.create(
            title="Dune",
            author=self.author,
            about_book="Desert planet politics",
            book_length=412
        )

    def test_book_list_returns_200(self):
        response = self.client.get(reverse('book_list'))
        self.assertEqual(response.status_code, 200)

    def test_book_list_shows_book_title(self):
        response = self.client.get(reverse('book_list'))
        self.assertContains(response, "Dune")

    def test_book_detail_returns_200(self):
        response = self.client.get(reverse('book_detail', args=[self.book.id]))
        self.assertEqual(response.status_code, 200)


class BookEditDeleteTest(TestCase):
    def setUp(self):
        self.author = Author.objects.create(name="Frank Herbert", bio="Sci-fi author")
        self.book = Book.objects.create(
            title="Dune",
            author=self.author,
            about_book="Desert planet politics",
            book_length=412
        )

    def test_edit_book(self):
        response = self.client.post(
            reverse('book_edit', args=[self.book.id]),
            {'title': 'Dune Messiah', 'author': self.author.id, 'about_book': 'Sequel', 'book_length': 300, 'tags': []}
        )
        self.book.refresh_from_db()
        self.assertEqual(self.book.title, 'Dune Messiah')

    def test_delete_book(self):
        response = self.client.post(reverse('book_delete', args=[self.book.id]))
        self.assertFalse(Book.objects.filter(id=self.book.id).exists())