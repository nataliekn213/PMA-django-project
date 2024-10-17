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
        fields = ['file',]

    def clean_file(self):
        file = self.cleaned_data.get('file')
        if file:
            allowed_extensions = ['txt', 'pdf', 'jpg']
            extension = file.split('.')[-1].lower()
            if extension not in allowed_extensions:
                raise forms.ValidationError("Only .txt, .pdf, and .jpg files are allowed.")
        return file