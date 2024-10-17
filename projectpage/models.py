from django.db import models

class Task(models.Model):
    task_title = models.CharField(max_length=150)
    deadline = models.DateTimeField("deadline")

    def __str__(self):
        return f"{self.task_title}: Due on {self.deadline}"

class Document(models.Model):
    file = models.FileField(upload_to='documents/')
    uploaded_at = models.DateTimeField(auto_now_add=True)