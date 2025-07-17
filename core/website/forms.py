from django import forms
from django.core.validators import RegexValidator
from .models import ContactMessage

class ContactModelForm(forms.ModelForm):
    phone_number = forms.CharField(
        required=False,
        max_length=11,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Phone Number (09xxxxxxxxx)'
        }),
        validators=[
            RegexValidator(
                regex=r'^09\d{9}$',
                message='Phone number must be 11 digits starting with 09',
                code='invalid_phone'
            ),
        ],
        label=''
    )

    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'phone_number', 'subject', 'message']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Your Name'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Your Email'
            }),
            'subject': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Subject (optional)'
            }),
            'message': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Your Message',
                'rows': 5
            }),
        }
        labels = {
            'name': '',
            'email': '',
            'subject': '',
            'message': '',
        }

    def clean_phone_number(self):
        phone_number = self.cleaned_data.get('phone_number')
        if phone_number:
            # Remove any non-digit characters
            phone_number = ''.join(filter(str.isdigit, phone_number))
            
            # Check if it starts with 09 and has 11 digits
            if not phone_number.startswith('09') or len(phone_number) != 11:
                raise forms.ValidationError("Please enter a valid Iranian phone number (11 digits starting with 09)")
            
            # Format as 09xxxxxxxxx
            return phone_number
        return phone_number

    def clean_message(self):
        message = self.cleaned_data['message']
        if len(message) < 10:
            raise forms.ValidationError("Message is too short. Please write at least 10 characters.")
        return message