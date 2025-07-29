from django import forms
from .models import Task, Category

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'due_date', 'category']
        widgets = {
            'due_date': forms.DateInput(attrs={'type': 'date'}),
            'completed_status': forms.CheckboxInput(),
        }
        labels = {
            'title': 'Task Title',
            'due_date': 'Due Date',
            'completed_status': 'Completed',
            'category': 'Category',
        }
