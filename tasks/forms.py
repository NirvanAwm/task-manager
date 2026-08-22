from django import forms
from .models import Task

class TaskForm(forms.ModelForm):
    class meta:
        model = Task
        fields = [
            'title',
            'description',
            'status',
            'priority',
        ]