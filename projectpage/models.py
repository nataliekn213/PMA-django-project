from django.db import models

class Task(models.Model):
    task_title = models.CharField(max_length=150)
    deadline = models.DateTimeField("deadline")

    def __str__(self):
        return f"{self.task_title}: Due on {self.deadline}"