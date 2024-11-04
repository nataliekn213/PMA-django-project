from django import forms
from django.forms import inlineformset_factory

from .models import Task, Document

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ["title", "deadline"]

class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ['file', 'title', 'description', 'keywords']

    def clean_file(self):
        file = self.cleaned_data.get('file')
        if file:
            allowed_extensions = ['txt', 'pdf', 'jpg']
            file_name = file.name
            # print(file_name)
            extension = file_name.split('.')[-1].lower()
            # print(extension)
            if extension not in allowed_extensions:
                raise forms.ValidationError("Only .txt, .pdf, and .jpg files are allowed.")
        return file