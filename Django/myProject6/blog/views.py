from django.shortcuts import render
from datetime import datetime

def blog_detail(request):
    
    post = {
        "title": "My Second Template Post",
        "description": "This is a description of my second template post.",
        "author": None,
        "created_at": datetime(2025, 1, 1, 12, 10, 30),
        "comments_count": 5,
        "tag": ["Python", "Django", "Web Development"],
        "price": 100,
        "number": 7,
    }
    return render(request, 'blog/blog_detail.html',{"post": post})


def blog_list(request):
    blogs =[
        {"title": "My First Template Post","is_featured": True, "author": "Dhwani Prasad "},
        {"title": "My First Template Post","is_featured": True, "author":"" },
        {"title": "My First Template Post","is_featured": True, "author": "Shlok"},
    ]
    context = {
        "blogs":blogs,
        "today": datetime.now(),
        "html_code": "<h1>My First Template Post</h1>",
    }
    return render(request, 'blog/blog_list.html', context)
