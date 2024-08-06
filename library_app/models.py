from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    is_librarian = models.BooleanField(default=False)
    is_reader = models.BooleanField(default=False)

class Librarian(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    employee_id = models.CharField(max_length=20, unique=True)

class Reader(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    address = models.TextField()

class Book(models.Model):
    title = models.CharField(max_length=50)
    author = models.CharField(max_length=50)
    genre = models.CharField(max_length=50)
    is_checked_out = models.BooleanField(default=False)

    def __str__(self):
        return self.title

class Borrowing(models.Model):
    reader = models.ForeignKey(Reader, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    borrowed_date = models.DateField(auto_now_add=True)
    returned_date = models.DateField(null=True, blank=True)

    def is_returned(self):
        return self.returned_date is not None
