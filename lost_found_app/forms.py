from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import LostItem, FoundItem

class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

class LostItemForm(forms.ModelForm):
    class Meta:
        model = LostItem
        fields = ['name', 'category', 'description', 'location', 'image']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Enter item name'}),
            'category': forms.Select(),
            'description': forms.Textarea(attrs={'placeholder': 'Enter description'}),
            'location': forms.TextInput(attrs={'placeholder': 'Enter location found'}),
            'image': forms.ClearableFileInput(),
        }

class FoundItemForm(forms.ModelForm):
    class Meta:
        model = FoundItem
        fields = ['name', 'category', 'description', 'location', 'image']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Enter item name'}),
            'category': forms.Select(),
            'description': forms.Textarea(attrs={'placeholder': 'Enter description'}),
            'location': forms.TextInput(attrs={'placeholder': 'Enter location found'}),
            'image': forms.ClearableFileInput(),
        }

# class LostIDCardForm(forms.ModelForm):
#     class Meta:
#         model = LostIDCard
#         fields = ['id_number', 'first_name', 'location']
#         widgets = {
#             'id_number': forms.TextInput(attrs={'placeholder': 'Enter ID number'}),
#             'first_name': forms.TextInput(attrs={'placeholder': 'Enter first name'}),
#             'location': forms.TextInput(attrs={'placeholder': 'Enter location lost'}),
#         }

# class FoundIDCardForm(forms.ModelForm):
#     class Meta:
#         model = FoundIDCard
#         fields = ['id_number', 'first_name', 'location']
#         widgets = {
#             'id_number': forms.TextInput(attrs={'placeholder': 'Enter ID number'}),
#             'first_name': forms.TextInput(attrs={'placeholder': 'Enter first name'}),
#             'location': forms.TextInput(attrs={'placeholder': 'Enter location found'}),
        # }