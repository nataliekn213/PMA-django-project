from django import forms
from django.forms import inlineformset_factory

from .models import Task, Document

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ["task_title", "deadline"]

class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ('file',)