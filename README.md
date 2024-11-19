# library_system

A Django-based application for managing a library system. It supports features like adding books, borrowing, returning, and tracking borrower history.

Book Management:
  Add new books.
  View all books with an optional filter for availability.
Borrowing and Returning:
  Borrow books by book_id and borrower_id.
  Return borrowed books.
Borrower History:
  List active (unreturned) books for a borrower.
  View the complete borrowing history of a borrower.

Prerequisites
  Python 3.x
  Django 4.x
  Virtual environment (.venv)

Setup Instructions

Clone the Repository:

  git clone https://github.com/your-username/library_system.git
  cd library_system
  Create and Activate a Virtual Environment:

  python -m venv venv
  source venv/bin/activate  
  For Windows: venv\Scripts\activate

After adding models run the following commands in terminal:
  python manage.py makemigrations
  python manage.py migrate

Run the Server:
  python manage.py runserver

 API Endpoints
 
Book Management
  POST /books/: Add a new book.
  GET /books/: List all books (optional filter: ?available=true).
  
Borrowing and Returning
  POST /borrow/: Borrow a book using book_id and borrower_id.
  POST /return/: Return a book using book_id.
  
Borrower History
  GET /borrowed/<borrower_id>/: List all active (unreturned) books for a borrower.
  GET /history/<borrower_id>/: List all books ever borrowed by the borrower (includes return status).


