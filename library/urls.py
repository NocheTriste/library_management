
from django.urls import path
from . import views

urlpatterns = [
    path('books/', views.book_list, name='book_list'),
    path('borrow/<int:book_id>/', views.borrow_book, name='borrow_book'),
    path('return/<int:loan_id>/', views.return_book, name='return_book'),
    path('my-loans/', views.my_loans, name='my_loans'),
    path('my-reservations/', views.my_reservations, name='my_reservations'),
    path('activity-log/', views.activity_log, name='activity_log'),
    path('add-book/', views.add_book, name='add_book'),
]