from django.utils import timezone
from .models import Book, Member, Loan, Reservation, ActivityLog

class LibraryServices:
    @staticmethod
    def borrow_book(book_id, member_id):
        """Método para prestar un libro (implementa lista enlazada)"""
        book = Book.objects.get(id=book_id)
        member = Member.objects.get(id=member_id)
        
        if book.available_copies > 0:
            # Crear nuevo préstamo
            new_loan = Loan.objects.create(
                book=book,
                member=member,
                loan_date=timezone.now()
            )
            
            # Actualizar disponibilidad
            book.available_copies -= 1
            book.save()
            
            # Registrar actividad (pila)
            ActivityLog.objects.create(
                user=member.user,
                action=f"Préstamo del libro: {book.title}"
            )
            
            return new_loan
        else:
            # Agregar a cola de reservas
            reservation = Reservation.objects.create(
                book=book,
                member=member
            )
            
            ActivityLog.objects.create(
                user=member.user,
                action=f"Reserva del libro: {book.title}"
            )
            
            return reservation

    @staticmethod
    def return_book(loan_id):
        """Método para devolver un libro (maneja lista y cola)"""
        loan = Loan.objects.get(id=loan_id)
        book = loan.book
        member = loan.member
        
        # Marcar como devuelto
        loan.return_date = timezone.now()
        loan.save()
        
        # Liberar copia
        book.available_copies += 1
        book.save()
        
        # Registrar actividad
        ActivityLog.objects.create(
            user=member.user,
            action=f"Devolución del libro: {book.title}"
        )
        
        # Procesar reservas (cola FIFO)
        pending_reservations = Reservation.objects.filter(
            book=book,
            is_active=True
        ).order_by('reservation_date')
        
        if pending_reservations.exists():
            next_reservation = pending_reservations.first()
            
            # Crear préstamo para la reserva más antigua
            new_loan = Loan.objects.create(
                book=book,
                member=next_reservation.member,
                loan_date=timezone.now()
            )
            
            # Marcar reserva como completada
            next_reservation.is_active = False
            next_reservation.save()
            
            # Actualizar disponibilidad
            book.available_copies -= 1
            book.save()
            
            ActivityLog.objects.create(
                user=next_reservation.member.user,
                action=f"Préstamo por reserva del libro: {book.title}"
            )
            
            return new_loan
        return None

    @staticmethod
    def get_member_activity(member_id, limit=10):
        """Obtiene el historial de actividades (pila LIFO)"""
        member = Member.objects.get(id=member_id)
        return ActivityLog.objects.filter(
            user=member.user
        ).order_by('-timestamp')[:limit]