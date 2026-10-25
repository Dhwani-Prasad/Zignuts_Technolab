from django.urls import path, re_path
from . import views

urlpatterns = [
    path('', views.home, name='blog-home'),
    path('about/', views.about, name='blog-about'),
    path('posts/<int:post_id>/', views.post_detail, name='blog-post-detail'),
    path('users/<str:username>/', views.user_profile, name='blog-user-profile'),
    # path('articles/<int:year>/<int:month>/', views.article_detail, name='blog-article-detail'),
    path('articles/<int:year>/<int:month>/<int:days>/', views.article_detail, name='blog-article-detail'),

    re_path(r'^articles/(?P<year>[0-9]{4})/$', views.articles_by_year, name='blog-articles-by-year'),
]