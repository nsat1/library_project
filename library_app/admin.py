from django.contrib import admin
from .models import User, Librarian, Reader, Book, Borrowing

admin.site.register(User)
admin.site.register(Librarian)
admin.site.register(Reader)
admin.site.register(Book)
admin.site.register(Borrowing)
