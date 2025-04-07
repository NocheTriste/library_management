from django.contrib import admin
from .models import Book, Member, Loan, Reservation, ActivityLog

admin.site.register(Book)
admin.site.register(Member)
admin.site.register(Loan)
admin.site.register(Reservation)
admin.site.register(ActivityLog)