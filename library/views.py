from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Book, Member, Loan, Reservation
from .services import LibraryServices
from.forms import BookForm

@login_required
def profile(request):
    return redirect('book_list')

@login_required
def book_list(request):
    books = Book.objects.all()
    return render(request, 'library/book_list.html', {'books': books})

@login_required
def borrow_book(request, book_id):
    member = Member.objects.get(user=request.user)
    LibraryServices.borrow_book(book_id, member.id)
    return redirect('book_list')

@login_required
def return_book(request, loan_id):
    LibraryServices.return_book(loan_id)
    return redirect('my_loans')

@login_required
def my_loans(request):
    member = Member.objects.get(user=request.user)
    active_loans = Loan.objects.filter(
        member=member,
        return_date__isnull=True
    )
    return render(request, 'library/my_loans.html', {'loans': active_loans})

@login_required
def my_reservations(request):
    member = Member.objects.get(user=request.user)
    reservations = Reservation.objects.filter(
        member=member,
        is_active=True
    ).order_by('reservation_date')
    return render(request, 'library/my_reservations.html', {'reservations': reservations})

@login_required
def activity_log(request):
    member = Member.objects.get(user=request.user)
    activities = LibraryServices.get_member_activity(member.id)
    return render(request, 'library/activity_log.html', {'activities': activities})


@login_required
def add_book(request):
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('book_list')  # Redirige a la lista de libros
    else:
        form = BookForm()
    
    return render(request, 'library/add_book.html', {'form': form})