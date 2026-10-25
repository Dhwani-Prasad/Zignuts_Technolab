from datetime import date, timedelta
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Task

User = get_user_model()

class TaskApiTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="tester", password="StrongPass123!")
        self.other_user = User.objects.create_user(username="other", password="StrongPass123!")
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {RefreshToken.for_user(self.user).access_token}")
        self.list_url = reverse("task-list")
        self.task = Task.objects.create(
            user=self.user,
            title="First task",
            description="Test description",
            due_date=date.today() + timedelta(days=2),
            priority="medium",
        )

    def test_list_tasks(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_create_task(self):
        response = self.client.post(self.list_url, {
            "title": "New task",
            "description": "Created in test",
            "due_date": str(date.today() + timedelta(days=3)),
            "priority": "high",
            "is_completed": False,
        }, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Task.objects.filter(user=self.user).count(), 2)

    def test_task_details(self):
        response = self.client.get(reverse("task-detail", args=[self.task.id]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_task(self):
        response = self.client.patch(reverse("task-detail", args=[self.task.id]), {
            "title": "Updated title"
        }, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.task.refresh_from_db()
        self.assertEqual(self.task.title, "Updated title")

    def test_delete_task(self):
        response = self.client.delete(reverse("task-detail", args=[self.task.id]))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Task.objects.filter(id=self.task.id).exists())

    def test_cannot_view_another_users_task(self):
        other_task = Task.objects.create(
            user=self.other_user,
            title="Private task",
            due_date=date.today() + timedelta(days=1),
            priority="low",
        )
        response = self.client.get(reverse("task-detail", args=[other_task.id]))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_unauthenticated_request_is_rejected(self):
        self.client.credentials()
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
