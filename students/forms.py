from django import forms
from .models import Student

class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['f_name', 'l_name', 'age', 'course_name', 'dept_name']
        labels = {
            'f_name': 'First Name',
            'l_name': 'Last Name',
            'age': 'Age',
            'course_name': 'Course Name',
            'dept_name': 'Department',
        }
        help_texts = {
            'age': 'Age must between 18 and 28',
        }
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'