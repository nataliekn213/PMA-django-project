from django import forms
from django.forms import inlineformset_factory

from .models import Task

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ["task_title", "deadline"]

