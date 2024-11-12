from django.db import models
from django.contrib.auth.models import User
from storages.backends.s3boto3 import S3Boto3Storage
    
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
    
class Project(models.Model):
    title = models.CharField(max_length=100, default="No Title")
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    members = models.ManyToManyField(User, through="Membership")

    def __str__(self):
        return f"{self.title}, owned by {self.owner}"
    
class Task(models.Model):
    title = models.CharField(max_length=200, default='Untitled Task')
    deadline = models.DateField()
    is_completed = models.BooleanField(default=False)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)

    def __str__(self):
        return self.title