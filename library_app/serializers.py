from rest_framework import serializers

from .models import Book, Borrowing


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['id', 'title', 'author', 'genre']


class BorrowingSerializer(serializers.ModelSerializer):
    book_title = serializers.CharField(source='book.title', read_only=True)
    days_borrowed = serializers.SerializerMethodField()

    class Meta:
        model = Borrowing
        fields = ['id', 'book_title', 'borrowed_date', 'days_borrowed']

    def get_days_borrowed(self, obj):

        return obj.days_borrowed()
