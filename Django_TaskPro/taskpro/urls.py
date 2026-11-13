from django.contrib import admin
from django.urls import path, include
from tasks.views import (
    home_view,
    login_view,
    register_view,
    dashboard_view,
)

urlpatterns = [
    path("admin/", admin.site.urls),
    # API endpoints under /api/
    path("api/", include("tasks.urls")),
    # Frontend pages
    path("", home_view, name="home"),
    path("login/", login_view, name="login"),
    path("register/", register_view, name="register"),
    path("dashboard/", dashboard_view, name="dashboard"),
]
