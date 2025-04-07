from django import forms
from .models import Book
from django.utils import timezone

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'author', 'isbn', 'category', 'total_copies', 'available_copies', 'publication_date']
        
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Título del libro'
            }),
            'author': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Autor del libro'
            }),
            'isbn': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'ISBN (13 caracteres)'
            }),
            'category': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Género/Categoría'
            }),
            'total_copies': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 1
            }),
            'available_copies': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 0
            }),
            'publication_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date',
                'max': timezone.now().date()
            }),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Asegurar que available_copies no sea mayor que total_copies
        if self.instance.pk:
            self.fields['available_copies'].widget.attrs['max'] = self.instance.total_copies