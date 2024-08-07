from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.contrib.auth.decorators import user_passes_test

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from drf_spectacular.utils import extend_schema

from .models import Book, Borrowing, Reader
from .forms import ReaderRegistrationForm
from .serializers import BookSerializer, BorrowingSerializer


def home(request):
    books = Book.objects.all().order_by('title')

    for book in books:
        book.is_borrowed = request.user.is_authenticated and Borrowing.objects.filter(book=book,
                                                                                      reader__user=request.user,
                                                                                      returned_date__isnull=True).exists()

    return render(request, 'home.html', {'books': books})


@login_required
def book_list(request):
    books = Book.objects.all()

    return render(request, 'book_list.html', {'books': books})


def register(request):

    if request.method == 'POST':
        form = ReaderRegistrationForm(request.POST)

        if form.is_valid():
            form.save()

            return redirect('login')
    else:
        form = ReaderRegistrationForm()

    return render(request, 'register.html', {'form': form})


def user_login(request):

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)

            return redirect('home')
        else:

            return render(request, 'login.html', {'error': 'Invalid credentials'})

    return render(request, 'login.html')


@login_required
def my_books(request):
    reader = Reader.objects.get(user=request.user)
    borrowings = Borrowing.objects.filter(reader=reader, returned_date__isnull=True).order_by('book__title')

    for borrowing in borrowings:
        borrowing.days_borrowed = (timezone.now().date() - borrowing.borrowed_date).days

    return render(request, 'my_books.html', {'borrowings': borrowings})


def user_logout(request):
    logout(request)

    return redirect('home')


@login_required
def borrow_book(request, book_id):

    if not request.user.is_reader:

        return redirect('home')

    book = Book.objects.get(id=book_id)
    reader = Reader.objects.get(user=request.user)
    Borrowing.objects.create(reader=reader, book=book)
    book.is_checked_out = True
    book.save()

    return redirect('home')


@login_required
def return_book(request, book_id):
    book = Book.objects.get(id=book_id)
    reader = Reader.objects.get(user=request.user)
    borrowing = Borrowing.objects.get(book=book, reader=reader, returned_date__isnull=True)
    borrowing.returned_date = timezone.now()
    borrowing.save()
    book.is_checked_out = False
    book.save()

    return redirect('home')


def librarian_login(request):

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None and user.is_librarian:
            login(request, user)

            return redirect('librarian_dashboard')
        else:

            return render(request, 'librarian_login.html', {'error': 'Invalid credentials'})

    return render(request, 'librarian_login.html')


@user_passes_test(lambda u: u.is_librarian)
def librarian_dashboard(request):
    overdue_borrowings = Borrowing.objects.filter(returned_date__isnull=True)

    for borrowing in overdue_borrowings:
        borrowing.days_overdue = borrowing.days_borrowed()

    return render(request, 'librarian_dashboard.html', {'overdue_borrowings': overdue_borrowings})


@extend_schema(
    responses=BookSerializer(many=True),
    description="Get a list of all books."
)
class BookListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        books = Book.objects.all()
        serializer = BookSerializer(books, many=True)

        return Response(serializer.data)


@extend_schema(
    responses=BorrowingSerializer,
    description="Borrow a book.",
    request=None,
    methods=['POST']
)
class BorrowBookView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, book_id):

        try:
            book = Book.objects.get(id=book_id)
        except Book.DoesNotExist:

            return Response({'error': 'Book not found'}, status=status.HTTP_404_NOT_FOUND)

        if book.is_checked_out:

            return Response({'error': 'Book is already borrowed'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            reader = Reader.objects.get(user=request.user)
        except Reader.DoesNotExist:

            return Response({'error': 'Reader not found'}, status=status.HTTP_404_NOT_FOUND)

        borrowing = Borrowing.objects.create(reader=reader, book=book)
        book.is_checked_out = True
        book.save()

        serializer = BorrowingSerializer(borrowing)

        return Response(serializer.data, status=status.HTTP_201_CREATED)


@extend_schema(
    responses=BorrowingSerializer,
    description="Return a borrowed book.",
    request=None,
    methods=['POST']
)
class ReturnBookView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, book_id):

        try:
            book = Book.objects.get(id=book_id)
        except Book.DoesNotExist:

            return Response({'error': 'Book not found'}, status=status.HTTP_404_NOT_FOUND)

        if not book.is_checked_out:

            return Response({'error': 'Book is not borrowed'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            reader = Reader.objects.get(user=request.user)
        except Reader.DoesNotExist:

            return Response({'error': 'Reader not found'}, status=status.HTTP_404_NOT_FOUND)

        try:
            borrowing = Borrowing.objects.get(reader=reader, book=book, returned_date__isnull=True)
        except Borrowing.DoesNotExist:

            return Response({'error': 'Borrowing record not found'}, status=status.HTTP_404_NOT_FOUND)

        borrowing.returned_date = timezone.now()
        borrowing.save()
        book.is_checked_out = False
        book.save()

        serializer = BorrowingSerializer(borrowing)

        return Response(serializer.data, status=status.HTTP_200_OK)


@extend_schema(
    responses=BorrowingSerializer(many=True),
    description="Get a list of books currently borrowed by the user."
)
class MyBooksView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):

        try:
            reader = Reader.objects.get(user=request.user)
        except Reader.DoesNotExist:

            return Response({'error': 'Reader not found'}, status=status.HTTP_404_NOT_FOUND)

        borrowings = Borrowing.objects.filter(reader=reader, returned_date__isnull=True)
        serializer = BorrowingSerializer(borrowings, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)
