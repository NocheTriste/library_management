from django.test import TestCase
from django.contrib.auth.models import User
from .models import Book, Member, Loan
from .services import LibraryServices
from datetime import date

class LibraryServicesTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.member = Member.objects.create(
            user=self.user,
            membership_id='M001',
            phone='1234567890',
            email='test@example.com'
        )
        self.book = Book.objects.create(
            title='Python for Beginners',
            author='John Doe',
            isbn='1234567890123',
            publication_date=date.today(),
            category='Programming',
            total_copies=2,
            available_copies=2
        )
    
    def test_borrow_book(self):
        # Prueba de préstamo exitoso
        loan = LibraryServices.borrow_book(self.book.id, self.member.id)
        self.assertIsNotNone(loan)
        self.book.refresh_from_db()
        self.assertEqual(self.book.available_copies, 1)
        
        # Prueba de reserva cuando no hay copias
        LibraryServices.borrow_book(self.book.id, self.member.id)  # 2do préstamo
        reservation = LibraryServices.borrow_book(self.book.id, self.member.id)  # Debería ser reserva
        self.assertIsNotNone(reservation)
        self.book.refresh_from_db()
        self.assertEqual(self.book.available_copies, 0)
    
    def test_return_book(self):
        # Préstamo y devolución
        loan = LibraryServices.borrow_book(self.book.id, self.member.id)
        returned = LibraryServices.return_book(loan.id)
        self.assertIsNone(returned)  # No hay reservas pendientes
        
        # Prueba con reserva pendiente
        LibraryServices.borrow_book(self.book.id, self.member.id)  # Agota copias
        reservation = LibraryServices.borrow_book(self.book.id, self.member.id)  # Crea reserva
        
        # Devuelve el libro (debería activar la reserva)
        loan = Loan.objects.filter(return_date__isnull=True).first()
        new_loan = LibraryServices.return_book(loan.id)
        self.assertIsNotNone(new_loan)