from rest_framework import serializers
from .models import Book, Author, Tag, ReadingLog

class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ['id', 'name', 'bio']


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name']

class BookSerializer(serializers.ModelSerializer):
    author = serializers.PrimaryKeyRelatedField(queryset=Author.objects.all())
    author_detail = AuthorSerializer(source='author', read_only=True)
    tags = serializers.PrimaryKeyRelatedField(many=True, queryset=Tag.objects.all(), required=False)
    tags_detail = TagSerializer(source='tags', many=True, read_only=True)

    class Meta:
        model = Book
        fields = ['id', 'title', 'author', 'author_detail', 'about_book', 'book_length', 'tags', 'tags_detail', 'created_at']