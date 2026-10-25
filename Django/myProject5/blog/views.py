from django.shortcuts import render
from datetime import datetime

class User:
    def __init__(self, username, age):
        self.username = username
        self.age = age 

def home(request):
    context = {
        "name": "Dhwani",
        "age": 22,
        "skills": ["Python", "Django", "JavaScript"],
        "user": User("Pooja", 24),
        "blog" : {
            "title": "My First Blog",
            "author": {
                "name": "Prasad",
            },
            "content": " <b> This is the content of my first blog post.</b> ",
            "date_posted": datetime.now(),
        },
        "empty_value": None,
    }
    return render(request, 'blog/home.html', context)