from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import BlogPost


class BlogPostForm(forms.ModelForm):
    class Meta:
        model = BlogPost  #It tells Django which model this form is based on
        fields = ["title", "content", "image"]  #It tells Django which model fields should appear in the form.
        widgets = {
            "title": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Enter blog title"
            }),
            "content": forms.Textarea(attrs={
                "class": "form-control",
                "rows": 8,
                "placeholder": "Write your blog here..."
            }),
            "image": forms.ClearableFileInput(attrs={
                "class": "form-control"
            }),
        }


class SignUpForm(UserCreationForm): # register a new user
    email = forms.EmailField(required=True)

    class Meta: # provides configuration information to Django
        model = User  # form creates a Django user
        fields = ["username", "email", "password1", "password2"]