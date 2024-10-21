from django.test import TestCase
import datetime
from django.utils import timezone
from django.urls import reverse, reverse_lazy
from django.contrib.auth.models import User

from .models import Task

class TaskCreation(TestCase):
    def test_task_creation(self):
        test_deadline = timezone.now() + datetime.timedelta(days=7)
        Task.objects.create(task_title="test_title", deadline=test_deadline)

        response = self.client.get(reverse_lazy("projectpage:task_list"))
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "projectpage/task_list.html")
        self.assertContains(response, "test_title")
    
class TaskDeletion(TestCase):
    def setUp(self):
        self.admin = User.objects.create_superuser("admin", "test@test.com", "password")