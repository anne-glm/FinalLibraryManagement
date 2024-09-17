from django.contrib import admin
from .models import Author, Book, Borrowing, Reservation, BookScore

class AuthorAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'biography', 'nationality', 'date_of_birth')

class BookAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'description', 'author', 'isbn', 'category', 'publication_date', 'average_score')
    search_fields = ('title', 'author__name', 'isbn', 'category')

  
    def average_score(self, obj):
        return obj.average_score()

    
    average_score.short_description = 'Average Score'

class BorrowingAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'book', 'borrow_date', 'due_date', 'return_date')
    list_filter = ('user', 'book')

    
    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

class ReservationAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'book', 'reserved_date')
    list_filter = ('user', 'book')

   
    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


admin.site.register(Author, AuthorAdmin)
admin.site.register(Book, BookAdmin)
admin.site.register(Borrowing, BorrowingAdmin)
admin.site.register(Reservation, ReservationAdmin)

