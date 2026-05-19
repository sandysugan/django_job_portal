from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    role = forms.ChoiceField(choices=CustomUser.ROLE_CHOICES)
    skills = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'e.g. Python, Django, SQL'}),
        help_text="Only for Job Seekers. Comma-separated."
    )

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'role', 'skills', 'password1', 'password2']