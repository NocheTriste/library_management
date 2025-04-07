from django.db import models
from django.contrib.auth.models import User

class Book(models.Model):
    """Representa un libro en la biblioteca (estructura de datos tipo registro/objeto)"""
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    isbn = models.CharField(max_length=13, unique=True)
    publication_date = models.DateField()
    category = models.CharField(max_length=50)
    total_copies = models.PositiveIntegerField(default=1)
    available_copies = models.PositiveIntegerField(default=1)
    
    def __str__(self):
        return f"{self.title} - {self.author}"

class Member(models.Model):
    """Representa un miembro de la biblioteca"""
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    membership_id = models.CharField(max_length=10, unique=True)
    phone = models.CharField(max_length=15)
    email = models.EmailField()
    
    def __str__(self):
        return f"{self.user.get_full_name()} ({self.membership_id})"

class Loan(models.Model):
    """Estructura tipo lista enlazada para préstamos"""
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    loan_date = models.DateTimeField(auto_now_add=True)
    return_date = models.DateTimeField(null=True, blank=True)
    next_loan = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True)
    
    class Meta:
        ordering = ['loan_date']
    
    def __str__(self):
        return f"Préstamo: {self.book} a {self.member}"

class Reservation(models.Model):
    """Estructura tipo cola (FIFO) para reservas"""
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    reservation_date = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['reservation_date']
    
    def __str__(self):
        return f"Reserva #{self.id} para {self.book}"

class ActivityLog(models.Model):
    """Estructura tipo pila (LIFO) para registro de actividades"""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    action = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-timestamp']
    
    def __str__(self):
        return f"{self.timestamp}: {self.action}"