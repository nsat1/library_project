from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model

from rest_framework.test import APITestCase, APIClient
from rest_framework import status

from .models import Book, Reader, Borrowing


User = get_user_model()

"""
Тесты для моделей
"""


class BookModelTest(TestCase):
    def setUp(self):
        self.book = Book.objects.create(title="Test Book", author="Test Author", genre="Test Genre")

    def test_book_creation(self):
        self.assertEqual(self.book.title, "Test Book")
        self.assertEqual(self.book.author, "Test Author")
        self.assertEqual(self.book.genre, "Test Genre")
        self.assertFalse(self.book.is_checked_out)


class ReaderModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="testpass")
        self.reader = Reader.objects.create(user=self.user, first_name="Test", last_name="Reader", address="Test Address")

    def test_reader_creation(self):
        self.assertEqual(self.reader.first_name, "Test")
        self.assertEqual(self.reader.last_name, "Reader")
        self.assertEqual(self.reader.address, "Test Address")
        self.assertEqual(str(self.reader), "Test Reader")


class BorrowingModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="testpass")
        self.reader = Reader.objects.create(user=self.user, first_name="Test", last_name="Reader", address="Test Address")
        self.book = Book.objects.create(title="Test Book", author="Test Author", genre="Test Genre")
        self.borrowing = Borrowing.objects.create(reader=self.reader, book=self.book)

    def test_borrowing_creation(self):
        self.assertEqual(self.borrowing.reader, self.reader)
        self.assertEqual(self.borrowing.book, self.book)
        self.assertIsNotNone(self.borrowing.borrowed_date)
        self.assertIsNone(self.borrowing.returned_date)
        self.assertFalse(self.borrowing.is_returned())

"""
Тесты для представлений
"""


class BookListViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username="testuser", password="testpass")
        self.client.force_authenticate(user=self.user)
        self.book = Book.objects.create(title="Test Book", author="Test Author", genre="Test Genre")

    def test_book_list_view(self):
        response = self.client.get(reverse('api_book_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Book")


class BorrowBookViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username="testuser", password="testpass")
        self.client.force_authenticate(user=self.user)
        self.reader = Reader.objects.create(user=self.user, first_name="Test", last_name="Reader", address="Test Address")
        self.book = Book.objects.create(title="Test Book", author="Test Author", genre="Test Genre")

    def test_borrow_book_view(self):
        response = self.client.post(reverse('api_borrow_book', args=[self.book.id]))
        self.assertEqual(response.status_code, 201)
        self.assertTrue(Borrowing.objects.filter(reader=self.reader, book=self.book).exists())

"""
Тесты для API
"""


class BookAPITest(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username="testuser", password="testpass")
        self.client.force_authenticate(user=self.user)
        self.book = Book.objects.create(title="Test Book", author="Test Author", genre="Test Genre")

    def test_book_list_api(self):
        response = self.client.get(reverse('api_book_list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(response, "Test Book")


class BorrowBookAPITest(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username="testuser", password="testpass")
        self.client.force_authenticate(user=self.user)
        self.reader = Reader.objects.create(user=self.user, first_name="Test", last_name="Reader", address="Test Address")
        self.book = Book.objects.create(title="Test Book", author="Test Author", genre="Test Genre")

    def test_borrow_book_api(self):
        response = self.client.post(reverse('api_borrow_book', args=[self.book.id]))
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Borrowing.objects.filter(reader=self.reader, book=self.book).exists())


"""
Тесты для админ-панели
"""


class AdminPanelTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.admin_user = User.objects.create_superuser(username="admin", password="adminpass", email="admin@example.com")
        self.client.login(username="admin", password="adminpass")
        self.book = Book.objects.create(title="Test Book", author="Test Author", genre="Test Genre")

    def test_book_admin_list(self):
        response = self.client.get(reverse('admin:library_app_book_changelist'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Book")

    def test_book_admin_add(self):
        response = self.client.post(reverse('admin:library_app_book_add'), {
            'title': 'New Book',
            'author': 'New Author',
            'genre': 'New Genre',
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Book.objects.filter(title="New Book").exists())
