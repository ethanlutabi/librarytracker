from django.db import models

# Create your models here.


class Author(models.Model):
    name = models.CharField(max_length=100)
    bio = models.TextField(blank=True)

    def __str__(self):
        return self.name


class Book(models.Model):
    title = models.CharField(max_length=100)
    author = models.ForeignKey('Author', on_delete=models.CASCADE, related_name='books')
    tags = models.ManyToManyField('Tag', related_name='books', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    about_book = models.TextField()
    book_length = models.IntegerField()

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title


class Tag(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class ReadingLog(models.Model):
    STATUS_CHOICES = [
        ('want', 'Want to Read'),
        ('reading', 'Reading'),
        ('finished', 'Finished'),
    ]
    book = models.ForeignKey('Book', on_delete=models.CASCADE, related_name='reading_logs')
    date = models.DateField()
    pages_read = models.IntegerField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='want')
    rating = models.IntegerField(null=True, blank=True)
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"{self.book.title} - {self.date} - {self.pages_read} pages"