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
    
class AdminStuff(TestCase):
    def setUp(self):
        self.admin = User.objects.create_superuser("admin", "test_admin@test.com", "admin_password")
        self.non_admin = User.objects.create_user("non_admin", "test_non_admin@test.com", "non_admin_password")
    
    def test_non_admin_dashboard(self):
        non_admin_login = self.client.login(username="non_admin", password="non_admin_password")
        self.assertTrue(non_admin_login)

        response = self.client.get(reverse_lazy("projectpage:admin_dashboard"))
        self.assertEqual(response.status_code, 403)

    def test_admin_dashboard(self):
        admin_login = self.client.login(username="admin", password="admin_password")
        self.assertTrue(admin_login)

        response = self.client.get(reverse_lazy("projectpage:admin_dashboard"))
        self.assertEqual(response.status_code, 200)

class TaskDeletion(TestCase):
    def setUp(self):
        self.admin = User.objects.create_superuser("admin", "test@test.com", "password")
        task = Task.objects.create(task_title="test_title", deadline=datetime.datetime.today())