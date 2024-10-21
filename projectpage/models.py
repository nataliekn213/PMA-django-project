from django.db import models
from storages.backends.s3boto3 import S3Boto3Storage

class Task(models.Model):
    title = models.CharField(max_length=200, default='Untitled Task')
    deadline = models.DateField()
    is_completed = models.BooleanField(default=False)
    def __str__(self):
        return self.title
class Document(models.Model):
    file = models.FileField(storage=S3Boto3Storage(), upload_to='documents/')
    uploaded_at = models.DateTimeField(auto_now_add=True)