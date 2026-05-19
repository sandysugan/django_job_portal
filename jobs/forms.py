from django import forms
from .models import Job

class JobForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = ['title', 'description', 'company', 'location', 'salary', 'required_skills', 'is_active']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 5}),
            'required_skills': forms.TextInput(attrs={'placeholder': 'e.g. Python, Django, React'}),
        }