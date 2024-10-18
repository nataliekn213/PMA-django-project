from django.db import models
from storages.backends.s3boto3 import S3Boto3Storage

class Task(models.Model):
    task_title = models.CharField(max_length=150)
    deadline = models.DateTimeField("deadline")

    def __str__(self):
        return f"{self.task_title}: Due on {self.deadline}"

class Document(models.Model):
    file = models.FileField(storage=S3Boto3Storage(), upload_to='documents/')
    uploaded_at = models.DateTimeField(auto_now_add=True)