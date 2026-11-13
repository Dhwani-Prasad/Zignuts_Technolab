from datetime import date, timedelta
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Task

User = get_user_model()


class TaskProApiTests(APITestCase):
    def setUp(self):
        # Create primary test user
        self.user1 = User.objects.create_user(
            username="user_one",
            email="user1@example.com",
            password="Password123!",
        )

        # Create secondary test user for data isolation testing
        self.user2 = User.objects.create_user(
            username="user_two",
            email="user2@example.com",
            password="Password123!",
        )

        # Obtain JWT token for user1
        login_res = self.client.post(
            reverse("auth-login"),
            {"username": "user_one", "password": "Password123!"},
            format="json",
        )
        self.assertEqual(login_res.status_code, status.HTTP_200_OK)
        self.token1 = login_res.data["access"]
        self.refresh1 = login_res.data["refresh"]

        # Authenticate client with user1 token
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.token1}")

        # Seed initial tasks for user1
        self.today = date.today()
        self.task1 = Task.objects.create(
            user=self.user1,
            title="Buy groceries",
            description="Milk, Bread, Butter",
            due_date=self.today + timedelta(days=2),
            priority="high",
            status="pending",
        )
        self.task2 = Task.objects.create(
            user=self.user1,
            title="Read Django documentation",
            description="Focus on DRF ViewSets and SimpleJWT",
            due_date=self.today + timedelta(days=5),
            priority="medium",
            status="completed",
        )
        self.task3 = Task.objects.create(
            user=self.user1,
            title="Pay electricity bill",
            description="Due before month end",
            due_date=self.today + timedelta(days=1),
            priority="low",
            status="pending",
        )

        # Seed a task for user2 (to verify isolation)
        self.other_task = Task.objects.create(
            user=self.user2,
            title="User2 Private Secret Task",
            description="Should never be visible to user1",
            due_date=self.today + timedelta(days=3),
            priority="high",
            status="pending",
        )

    # -------------------------------------------------------------------------
    # User Management Tests
    # -------------------------------------------------------------------------
    def test_registration_success(self):
        """Test successful registration with password confirmation."""
        url = reverse("auth-register")
        payload = {
            "username": "new_user",
            "email": "newuser@example.com",
            "password": "SecurePassword123!",
            "password_confirm": "SecurePassword123!",
        }
        res = self.client.post(url, payload, format="json")
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.filter(username="new_user").exists())

    def test_registration_password_mismatch(self):
        """Test registration validation failure on mismatched passwords."""
        url = reverse("auth-register")
        payload = {
            "username": "mismatch_user",
            "email": "mismatch@example.com",
            "password": "Password123!",
            "password_confirm": "DifferentPassword123!",
        }
        res = self.client.post(url, payload, format="json")
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("password_confirm", res.data)

    def test_login_jwt(self):
        """Test login returns access and refresh JWT tokens."""
        url = reverse("auth-login")
        payload = {"username": "user_one", "password": "Password123!"}
        res = self.client.post(url, payload, format="json")
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn("access", res.data)
        self.assertIn("refresh", res.data)

    def test_token_refresh(self):
        """Test JWT token refresh endpoint."""
        url = reverse("auth-refresh")
        res = self.client.post(url, {"refresh": self.refresh1}, format="json")
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn("access", res.data)

    def test_unauthenticated_user_denied(self):
        """Ensure unauthenticated requests to tasks endpoints are rejected."""
        self.client.credentials()  # Remove auth headers
        url = reverse("task-list")
        res = self.client.get(url)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    # -------------------------------------------------------------------------
    # Task Management Tests
    # -------------------------------------------------------------------------
    def test_create_task(self):
        """Test creating a task with title, description, priority, due date, status."""
        url = reverse("task-list")
        payload = {
            "title": "Clean Workspace",
            "description": "Organize desk and files",
            "due_date": str(self.today + timedelta(days=3)),
            "priority": "medium",
            "status": "pending",
        }
        res = self.client.post(url, payload, format="json")
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(res.data["title"], "Clean Workspace")
        self.assertEqual(res.data["priority"], "medium")
        self.assertEqual(res.data["status"], "pending")
        self.assertEqual(res.data["user"], "user_one")

    def test_user_data_isolation(self):
        """Verify user1 CANNOT see or access user2's tasks."""
        url = reverse("task-list")
        res = self.client.get(url)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        titles = [item["title"] for item in res.data]
        self.assertNotIn("User2 Private Secret Task", titles)

        # Attempt to directly access user2's task by ID
        detail_url = reverse("task-detail", kwargs={"pk": self.other_task.id})
        res = self.client.get(detail_url)
        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)

        # Attempt to delete user2's task
        res = self.client.delete(detail_url)
        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)

    def test_filter_by_status(self):
        """Test filtering tasks by status: completed, pending, all."""
        url = reverse("task-list")

        # Pending filter
        res = self.client.get(f"{url}?status=pending")
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        for item in res.data:
            self.assertEqual(item["status"], "pending")
        self.assertEqual(len(res.data), 2)

        # Completed filter
        res = self.client.get(f"{url}?status=completed")
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        for item in res.data:
            self.assertEqual(item["status"], "completed")
        self.assertEqual(len(res.data), 1)

    def test_filter_by_priority(self):
        """Test filtering tasks by priority: high, medium, low."""
        url = reverse("task-list")
        res = self.client.get(f"{url}?priority=high")
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        for item in res.data:
            self.assertEqual(item["priority"], "high")

    def test_search_by_title(self):
        """Test searching tasks by title substring."""
        url = reverse("task-list")
        res = self.client.get(f"{url}?search=groceries")
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]["title"], "Buy groceries")

    def test_date_based_sorting_ascending(self):
        """Test tasks are sorted by due date ascending by default."""
        url = reverse("task-list")
        res = self.client.get(url)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        due_dates = [item["due_date"] for item in res.data]
        self.assertEqual(due_dates, sorted(due_dates))

    def test_edit_task(self):
        """Test updating an existing task."""
        url = reverse("task-detail", kwargs={"pk": self.task1.id})
        payload = {
            "title": "Buy groceries & vegetables",
            "description": "Updated grocery list",
            "due_date": str(self.today + timedelta(days=1)),
            "priority": "high",
            "status": "pending",
        }
        res = self.client.put(url, payload, format="json")
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.task1.refresh_from_db()
        self.assertEqual(self.task1.title, "Buy groceries & vegetables")
        self.assertEqual(self.task1.description, "Updated grocery list")

    def test_delete_task(self):
        """Test deleting a task."""
        url = reverse("task-detail", kwargs={"pk": self.task3.id})
        res = self.client.delete(url)
        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Task.objects.filter(id=self.task3.id).exists())

    def test_mark_task_as_completed(self):
        """Test marking a task as completed via complete action endpoint."""
        url = reverse("task-complete", kwargs={"pk": self.task1.id})
        res = self.client.patch(url)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data["status"], "completed")
        self.task1.refresh_from_db()
        self.assertEqual(self.task1.status, "completed")

    def test_toggle_task_status(self):
        """Test toggling task status between pending and completed."""
        url = reverse("task-toggle", kwargs={"pk": self.task1.id})
        # task1 is pending, should become completed
        res = self.client.patch(url)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data["status"], "completed")

        # toggle again, should become pending
        res2 = self.client.patch(url)
        self.assertEqual(res2.status_code, status.HTTP_200_OK)
        self.assertEqual(res2.data["status"], "pending")

    def test_stats_endpoint(self):
        """Test stats endpoint returns accurate counts for dashboard."""
        url = reverse("task-stats")
        res = self.client.get(url)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data["total"], 3)
        self.assertEqual(res.data["completed"], 1)
        self.assertEqual(res.data["pending"], 2)
        self.assertEqual(res.data["high_priority"], 1)
