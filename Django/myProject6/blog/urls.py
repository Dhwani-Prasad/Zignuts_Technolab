from django.urls import path
from . import views

urlpatterns = [
    path('details/', views.blog_detail, name='blog_detail'), 
    path('', views.blog_list, name='blog_list'), 
]