from django.test import TestCase
from datetime import datetime
from django.utils import timezone
from django.urls import reverse

from .models import Task

class TaskModelTests(TestCase):
    def task_testing(self):
        test_deadline = timezone.now() + datetime.timedelta(days=7)
        task = Task(task_title="test_title", deadline=test_deadline)

        response = self.client.get()