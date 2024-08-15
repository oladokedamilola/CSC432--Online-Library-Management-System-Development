from django import forms
from .models import Reader

class ReaderForm(forms.ModelForm):
    class Meta:
        model = Reader
        fields = ['name', 'phone_number', 'reference_id', 'address', 'is_active']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control'}),
            'reference_id': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
