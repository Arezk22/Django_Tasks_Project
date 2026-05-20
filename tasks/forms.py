from django import forms
from .models import Task
from django.utils import timezone

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title','description','status','priority','completed','due_date']
        labels={
            'title':'Title',
            'description':'Description',
            'status':'Status',
            'priority':'Priority',
            'completed':'Is_Completed',
            'due_date':'due_date'
        }
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'what you want'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control', 
                'placeholder': 'Add more Details ...',
                'rows': 3
            }),
            'status': forms.Select(attrs={'class': 'form-select'}),
            'priority': forms.Select(attrs={'class': 'form-select'}),
            'completed': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'due_date': forms.DateInput(attrs={
                'class': 'form-control', 
                'type': 'date' 
            }),
        }

    def clean_due_date(self):
        due_date = self.cleaned_data.get('due_date')
        
        # Check if due_date is not None and if it's in the past
        if due_date and due_date < timezone.now().date():
            raise forms.ValidationError('Due date cannot be in the past.')
        
        return due_date