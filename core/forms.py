from django import forms

from .models import Application, ContactMessage


class ApplicationForm(forms.ModelForm):
    images = forms.ImageField(required=False, widget=forms.FileInput(attrs={
        'class': 'w-full px-4 py-3 rounded-lg bg-gray-800 border border-gray-700 text-gray-400 focus:outline-none focus:border-amber-500 transition-colors file:mr-4 file:py-2 file:px-4 file:rounded-full file:border-0 file:text-sm file:font-semibold file:bg-amber-500 file:text-black file:cursor-pointer file:transition-colors',
    }))

    class Meta:
        model = Application
        fields = ['name', 'age', 'email', 'phone', 'location', 'application_type', 'experience', 'images']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 rounded-lg bg-gray-800 border border-gray-700 text-white placeholder-gray-400 focus:outline-none focus:border-amber-500 transition-colors',
                'placeholder': 'Your Full Name'
            }),
            'age': forms.NumberInput(attrs={
                'class': 'w-full px-4 py-3 rounded-lg bg-gray-800 border border-gray-700 text-white placeholder-gray-400 focus:outline-none focus:border-amber-500 transition-colors',
                'placeholder': 'Your Age',
                'min': '18',
                'max': '50'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'w-full px-4 py-3 rounded-lg bg-gray-800 border border-gray-700 text-white placeholder-gray-400 focus:outline-none focus:border-amber-500 transition-colors',
                'placeholder': 'your.email@example.com'
            }),
            'phone': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 rounded-lg bg-gray-800 border border-gray-700 text-white placeholder-gray-400 focus:outline-none focus:border-amber-500 transition-colors',
                'placeholder': '+1 (555) 000-0000'
            }),
            'location': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 rounded-lg bg-gray-800 border border-gray-700 text-white placeholder-gray-400 focus:outline-none focus:border-amber-500 transition-colors',
                'placeholder': 'City, Country'
            }),
            'application_type': forms.Select(attrs={
                'class': 'w-full px-4 py-3 rounded-lg bg-gray-800 border border-gray-700 text-white focus:outline-none focus:border-amber-500 transition-colors'
            }),
            'experience': forms.Textarea(attrs={
                'class': 'w-full px-4 py-3 rounded-lg bg-gray-800 border border-gray-700 text-white placeholder-gray-400 focus:outline-none focus:border-amber-500 transition-colors',
                'placeholder': 'Tell us about your modeling experience...',
                'rows': 5
            }),
        }


class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'message']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 rounded-lg bg-gray-800 border border-gray-700 text-white placeholder-gray-400 focus:outline-none focus:border-amber-500 transition-colors',
                'placeholder': 'Your Name'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'w-full px-4 py-3 rounded-lg bg-gray-800 border border-gray-700 text-white placeholder-gray-400 focus:outline-none focus:border-amber-500 transition-colors',
                'placeholder': 'your.email@example.com'
            }),
            'message': forms.Textarea(attrs={
                'class': 'w-full px-4 py-3 rounded-lg bg-gray-800 border border-gray-700 text-white placeholder-gray-400 focus:outline-none focus:border-amber-500 transition-colors',
                'placeholder': 'Your Message',
                'rows': 5
            }),
        }