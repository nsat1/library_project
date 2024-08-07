from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('books/', views.book_list, name='book_list'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('borrow/<int:book_id>/', views.borrow_book, name='borrow_book'),
    path('return/<int:book_id>/', views.return_book, name='return_book'),
    path('my_books/', views.my_books, name='my_books'),
    path('librarian/login/', views.librarian_login, name='librarian_login'),
    path('librarian/dashboard/', views.librarian_dashboard, name='librarian_dashboard'),
    path('api/books/', views.BookListView.as_view(), name='api_book_list'),
    path('api/borrow/<int:book_id>/', views.BorrowBookView.as_view(), name='api_borrow_book'),
    path('api/return/<int:book_id>/', views.ReturnBookView.as_view(), name='api_return_book'),
    path('api/my_books/', views.MyBooksView.as_view(), name='api_my_books'),
]
