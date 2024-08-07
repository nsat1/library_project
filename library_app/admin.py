from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from simple_history.admin import SimpleHistoryAdmin

from .models import User, Book, Borrowing, HistoricalBook


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ('username', 'email', 'is_staff', 'is_active', 'date_joined')
    search_fields = ('username', 'email')
    list_filter = ('is_staff', 'is_active', 'date_joined')
    ordering = ('-date_joined',)

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2'),
        }),
    )


@admin.register(Book)
class BookAdmin(SimpleHistoryAdmin):
    list_display = ('title', 'author', 'genre', 'is_checked_out')
    search_fields = ('title', 'author', 'genre')
    list_filter = ('genre', 'is_checked_out')
    ordering = ('title',)


@admin.register(Borrowing)
class BorrowingAdmin(admin.ModelAdmin):
    list_display = ('reader', 'book', 'borrowed_date', 'returned_date')
    search_fields = ('reader__user__username', 'book__title')
    list_filter = ('borrowed_date', 'returned_date')
    ordering = ('-borrowed_date',)

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.select_related('reader', 'book')

        return queryset


admin.site.register(HistoricalBook, SimpleHistoryAdmin)
