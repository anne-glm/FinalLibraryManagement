#books/urls.py
from django.urls import path
from .views import (
    AuthorListCreateView, AuthorRetrieveUpdateDestroyView,
    BookListView, BookCreateView, BookRetrieveUpdateDestroyView,
    BorrowBookView, ReturnBookView, ReserveBookView,
    UserRegistrationView, BorrowedBooksListView, BookScoreCreateView,
    ReservedBooksListView  
)

urlpatterns = [
    path('authors/', AuthorListCreateView.as_view(), name='author-list-create'),
    path('authors/<int:pk>/', AuthorRetrieveUpdateDestroyView.as_view(), name='author-detail'),
    path('books/', BookListView.as_view(), name='book-list'),
    path('books/score/', BookScoreCreateView.as_view(), name='book-score'),
    path('books/create/', BookCreateView.as_view(), name='book-create'),
    path('books/<int:pk>/', BookRetrieveUpdateDestroyView.as_view(), name='book-detail'),
    path('borrow/', BorrowBookView.as_view(), name='borrow-book'),
    path('return/<int:pk>/', ReturnBookView.as_view(), name='return-book'),
    path('reserve/', ReserveBookView.as_view(), name='reserve-book'),
    path('register/', UserRegistrationView.as_view(), name='user-register'),
    path('reserved-books/', ReservedBooksListView.as_view(), name='reserved-books-list'),
    path('borrowed-books/', BorrowedBooksListView.as_view(), name='borrowed-books-list'),
]
