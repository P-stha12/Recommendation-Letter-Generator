from django import forms
from home.models import StudentLoginInfo

class StudentForm(forms.ModelForm):
    username = forms.CharField(max_length=120, help_text="Enter Name:")
    roll_number = forms.CharField(max_length=9, help_text="Roll no: ")
    dob = forms.DateField(help_text="Date of Birth")
    gender = forms.CharField(max_length=10, help_text="Gender")

    class Meta:
        model = StudentLoginInfo
        exclude = ('department','program',)
