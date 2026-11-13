from datetime import date
from django.contrib.auth import get_user_model
from django.shortcuts import render, redirect
from rest_framework import generics, viewsets, permissions, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Task
from .serializers import RegisterSerializer, UserSerializer, TaskSerializer
from .permissions import IsTaskOwner

User = get_user_model()


# --------------------------------------------------------------------------
# API Views
# --------------------------------------------------------------------------

class RegisterView(generics.CreateAPIView):
    """
    API endpoint for new user registration.
    """
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]


class CurrentUserView(generics.RetrieveAPIView):
    """
    API endpoint to retrieve the currently authenticated user's profile.
    """
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user


class TaskViewSet(viewsets.ModelViewSet):
    """
    ViewSet for full CRUD operations on tasks.
    Enforces user-level data isolation, search, filtering, and sorting.
    """
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated, IsTaskOwner]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["title", "description"]
    ordering_fields = ["due_date", "priority", "created_at", "title", "status"]
    ordering = ["due_date", "created_at"]

    def get_queryset(self):
        """
        Always isolate tasks by the authenticated user.
        Supports status (all, completed, pending) and priority (low, medium, high) filters.
        """
        # User isolation
        queryset = Task.objects.filter(user=self.request.user)

        # Status filter
        status_param = self.request.query_params.get("status", "").strip().lower()
        if status_param in ["completed", "pending"]:
            queryset = queryset.filter(status=status_param)

        # Priority filter
        priority_param = self.request.query_params.get("priority", "").strip().lower()
        if priority_param in ["low", "medium", "high"]:
            queryset = queryset.filter(priority=priority_param)

        return queryset

    def perform_create(self, serializer):
        """
        Automatically bind the newly created task to the logged-in user.
        """
        serializer.save(user=self.request.user)

    @action(detail=True, methods=["patch", "post"])
    def complete(self, request, pk=None):
        """
        Mark a specific task as completed.
        """
        task = self.get_object()
        task.status = "completed"
        task.save(update_fields=["status", "updated_at"])
        serializer = self.get_serializer(task)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=["patch", "post"])
    def toggle(self, request, pk=None):
        """
        Toggle a task between pending and completed.
        """
        task = self.get_object()
        task.status = "completed" if task.status == "pending" else "pending"
        task.save(update_fields=["status", "updated_at"])
        serializer = self.get_serializer(task)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=["get"])
    def stats(self, request):
        """
        Retrieve task statistics for the authenticated user's dashboard.
        """
        tasks = Task.objects.filter(user=request.user)
        today = date.today()
        total_count = tasks.count()
        completed_count = tasks.filter(status="completed").count()
        pending_count = tasks.filter(status="pending").count()
        high_priority_count = tasks.filter(priority="high", status="pending").count()
        overdue_count = tasks.filter(status="pending", due_date__lt=today).count()
        due_today_count = tasks.filter(status="pending", due_date=today).count()

        return Response(
            {
                "total": total_count,
                "completed": completed_count,
                "pending": pending_count,
                "high_priority": high_priority_count,
                "overdue": overdue_count,
                "due_today": due_today_count,
            },
            status=status.HTTP_200_OK,
        )


# --------------------------------------------------------------------------
# Frontend Template Views
# --------------------------------------------------------------------------

def home_view(request):
    """Entry page: redirect to login or dashboard."""
    return render(request, "index.html")

def login_view(request):
    """Render login page."""
    return render(request, "login.html")

def register_view(request):
    """Render registration page."""
    return render(request, "register.html")

def dashboard_view(request):
    """Render main task dashboard."""
    return render(request, "dashboard.html")
