from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import Book, Borrowing, Reader
from .forms import ReaderRegistrationForm
from django.utils import timezone


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
        return redirect('home')  # или другой URL, куда вы хотите перенаправить нечитателей

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