from django.contrib.auth import get_user_model
from rest_framework import generics, viewsets, permissions, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Task
from .serializers import RegisterSerializer, TaskSerializer
from .permissions import IsTaskOwner

User = get_user_model()

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]
    throttle_classes = []

class TaskViewSet(viewsets.ModelViewSet):
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated, IsTaskOwner]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["title", "description", "priority"]
    ordering_fields = ["due_date", "created_at", "priority"]
    ordering = ["due_date"]

    def get_queryset(self):
        queryset = Task.objects.filter(user=self.request.user)
        status = self.request.query_params.get("status")
        if status == "completed":
            queryset = queryset.filter(is_completed=True)
        elif status == "pending":
            queryset = queryset.filter(is_completed=False)
        priority = self.request.query_params.get("priority")
        if priority in ["low", "medium", "high"]:
            queryset = queryset.filter(priority=priority)
        return queryset

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=True, methods=["patch"])
    def complete(self, request, pk=None):
        task = self.get_object()
        task.is_completed = True
        task.save(update_fields=["is_completed", "updated_at"])
        return Response(self.get_serializer(task).data)
