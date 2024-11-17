from django import forms
from django.forms import inlineformset_factory
from django.contrib import admin
from django.contrib.auth.models import User

from .models import Task, Document, Project

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
            # print(file_name);
            extension = file_name.split('.')[-1].lower()
            # print(extension)
            if extension not in allowed_extensions:
                raise forms.ValidationError("Only .txt, .pdf, and .jpg files are allowed.")
        return file

class ProjectForm(forms.ModelForm):
    members = forms.ModelMultipleChoiceField(
        queryset=User.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=True
    )

    tasks = forms.ModelMultipleChoiceField(
        queryset=Task.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = Project
        fields = ["title", "owner", "members", "tasks"]

    def save(self, commit=True):
        project = super().save(commit=False)
        if commit:
            project.save()
            # project.members.set(self.cleaned_data["members"])
            self.cleaned_data["tasks"].update(project=project)
        return project