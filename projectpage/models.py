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
    title = models.CharField(max_length=50, default="No title")
    uploaded_at = models.DateTimeField(auto_now_add=True)
    description = models.CharField(max_length=150, default="No description")
    keywords = models.TextField(default="No keywords")
    # comment

    def __str__(self):
        return f'''{self.title} uploaded on {self.uploaded_at} to {self.file.url}, 
        with description {self.description} and keywords: {self.keywords}'''

# django-admin - be able to change user status (common/pma)
class CustomUser(models.Model):
    user = models.OneToOneField(User, on_delete+models.CASCADE)
    is_pma = models.BooleanField(default=False)