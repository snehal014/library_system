from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),  # Home page
    path('books/', views.list_books, name='list_books'),
    path('books/add/', views.add_book, name='add_book'),
    path('borrow/', views.borrow_book, name='borrow_book'),
    path('return/', views.return_book, name='return_book'),
    path('borrowed/<int:borrower_id>/', views.borrowed_books, name='borrowed_books'),
    path('history/<int:borrower_id>/', views.borrower_history, name='borrower_history'),
]
