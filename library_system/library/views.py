from django.shortcuts import get_object_or_404
from django.http import JsonResponse,HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Book, Borrower, Loan
from django.utils import timezone

def home(request):
    return HttpResponse("<h1>Welcome to Library System</h1>")

@api_view(['POST'])
def add_book(request):
    title = request.data.get('title')
    author = request.data.get('author')
    book = Book.objects.create(title=title, author=author)
    return JsonResponse({"message": "Book added successfully", "book": {"id": book.id, "title": book.title}})


@api_view(['GET'])
def list_books(request):
    available = request.GET.get('available')
    books = Book.objects.all()
    if available:
        books = books.filter(available=True if available == 'true' else False)
    book_list = [{"id": book.id, "title": book.title, "author": book.author} for book in books]
    return JsonResponse(book_list, safe=False)


@api_view(['POST'])
def borrow_book(request):
    book_id = request.data.get('book_id')
    borrower_id = request.data.get('borrower_id')

    book = get_object_or_404(Book, id=book_id)
    borrower = get_object_or_404(Borrower, id=borrower_id)

    if not borrower.is_active:
        return JsonResponse({"error": "Borrower is not active"}, status=400)

    if book.available == False:
        return JsonResponse({"error": "Book is unavailable"}, status=400)

    active_loans = Loan.objects.filter(borrower=borrower, is_returned=False)
    if active_loans.count() >= 3:
        return JsonResponse({"error": "Borrower has reached the borrowing limit of 3 books"}, status=400)

    loan = Loan.objects.create(
        book=book,
        borrower=borrower,
        return_due=timezone.now() + timezone.timedelta(days=14)  # Set return due to 14 days
    )

    book.available = False
    book.borrow_count += 1
    book.save()

    return JsonResponse(
        {"message": "Book borrowed successfully", "loan": {"book": book.title, "borrower": borrower.name}})


@api_view(['POST'])
def return_book(request):
    book_id = request.data.get('book_id')
    borrower_id = request.data.get('borrower_id')

    loan = get_object_or_404(Loan, book_id=book_id, borrower_id=borrower_id, is_returned=False)

    loan.returned_on = timezone.now()
    loan.is_returned = True
    loan.save()

    book = loan.book
    book.available = True
    book.save()

    return JsonResponse({"message": "Book returned successfully"})


@api_view(['GET'])
def borrowed_books(request, borrower_id):
    borrower = get_object_or_404(Borrower, id=borrower_id)
    loans = Loan.objects.filter(borrower=borrower, is_returned=False)
    borrowed_books = [{"book": loan.book.title, "borrowed_on": loan.borrowed_on} for loan in loans]
    return JsonResponse(borrowed_books, safe=False)


@api_view(['GET'])
def borrower_history(request, borrower_id):
    borrower = get_object_or_404(Borrower, id=borrower_id)
    loans = Loan.objects.filter(borrower=borrower)
    history = [{"book": loan.book.title, "borrowed_on": loan.borrowed_on, "returned_on": loan.returned_on,
                "is_returned": loan.is_returned} for loan in loans]
    return JsonResponse(history, safe=False)
