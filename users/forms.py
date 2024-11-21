from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser, UserInterest, Onboarding
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator

class CustomUserCreationForm(UserCreationForm):
    first_name = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs={'placeholder': 'Enter your first name'})
    )
    last_name = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs={'placeholder': 'Enter your last name'})
    )

    country = forms.ChoiceField(
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'username', 'email', 'country', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        countries = kwargs.pop('countries', [])
        super().__init__(*args, **kwargs)
        self.fields['country'].choices = countries

    def clean_first_name(self):
        first_name = self.cleaned_data.get('first_name')
        if not first_name.isalpha():
            raise ValidationError("First name must contain only letters.")
        return first_name

    def clean_last_name(self):
        last_name = self.cleaned_data.get('last_name')
        if not last_name.isalpha():
            raise ValidationError("Last name must contain only letters.")
        return last_name

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if CustomUser.objects.filter(email=email).exists():
            raise ValidationError("A user with this email already exists.")
        return email

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        # Check if passwords match
        if password1 and password2 and password1 != password2:
            raise ValidationError("Passwords do not match.")

        # Minimum length requirement
        if len(password1) < 8:
            raise ValidationError("Password must be at least 8 characters long.")

        # Require both letters and numbers
        if not any(char.isdigit() for char in password1):
            raise ValidationError("Password must contain at least one numeral.")
        if not any(char.isalpha() for char in password1):
            raise ValidationError("Password must contain at least one letter.")

        # Optional: Require at least one special character
        special_characters = "!@#$%^&*()-+"
        if not any(char in special_characters for char in password1):
            raise ValidationError("Password must contain at least one special character.")

        return password2

class CustomLoginForm(forms.Form):
    username = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your username'
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your password'
        })
    )

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if not username:
            raise ValidationError("Username is required.")
        if len(username) < 5:
            raise ValidationError("Username must be at least 5 characters long.")
        return username

    def clean_password(self):
        password = self.cleaned_data.get('password')
        if not password:
            raise ValidationError("Password is required.")
        if len(password) < 8:
            raise ValidationError("Password must be at least 8 characters long.")
        return password
    

from django import forms
from .models import Onboarding, UserInterest

class OnboardingStep1Form(forms.ModelForm):
    is_student = forms.BooleanField(required=False, label="Are you a student?")

    class Meta:
        model = Onboarding
        fields = ['is_student']

class OnboardingStep2Form(forms.Form):
    interests = forms.CharField(widget=forms.HiddenInput(), required=True)

    def clean_interests(self):
        interests = self.cleaned_data.get('interests')
        interests_ids = interests.split(",")  # Split the comma-separated string
        if len(interests_ids) < 3:
            raise forms.ValidationError("You must select at least 3 interests.")
        if len(interests_ids) > 5:
            raise forms.ValidationError("You can select up to 5 interests.")
        # Ensure all selected interests are valid UserInterest IDs
        valid_ids = UserInterest.objects.filter(id__in=interests_ids).values_list('id', flat=True)
        if len(valid_ids) != len(interests_ids):
            raise forms.ValidationError("Some of the selected interests are invalid.")
        return interests


class OnboardingStep3Form(forms.ModelForm):
    goal = forms.ChoiceField(
        choices=[
            ('knowledge', 'To expand my knowledge and skills'), 
            ('entertainment', 'For personal enjoyment and relaxation'),
            ('education', 'To enhance my academic understanding and performance'),
            ('career', 'To improve my career prospects and professional growth'),
            ('social_interaction', 'To engage with and learn from others'),
            ('personal_growth', 'For personal growth and self-development')
        ],
        required=True
    )

    class Meta:
        model = Onboarding
        fields = ['goal']


class UserProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['profile_image']