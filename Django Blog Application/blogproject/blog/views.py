from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render

from .forms import BlogPostForm, SignUpForm
from .models import BlogPost


def home(request):
    query = request.GET.get("q", "").strip()
    posts = BlogPost.objects.select_related("author").all()

    if query:
        posts = posts.filter(
            Q(title__icontains=query) |
            Q(content__icontains=query)
        )

    paginator = Paginator(posts, 4)
    page_obj = paginator.get_page(request.GET.get("page"))

    return render(request, "home.html", {
        "page_obj": page_obj,
        "query": query
    })


def post_detail(request, pk):
    post = get_object_or_404(
        BlogPost.objects.select_related("author"),
        pk=pk
    )
    return render(request, "post_detail.html", {"post": post})


@login_required
def post_create(request):
    if request.method == "POST":
        form = BlogPostForm(request.POST, request.FILES)

        if form.is_valid():
            post = form.save(commit=False) # to set author
            post.author = request.user
            post.save()
            messages.success(request, "Blog post created successfully.")
            return redirect(post.get_absolute_url())
    else:
        form = BlogPostForm()

    return render(request, "post_form.html", {
        "form": form,
        "title": "Create Blog Post"
    })


@login_required
def post_edit(request, pk):
    post = get_object_or_404(
        BlogPost,
        pk=pk,
        author=request.user
    )

    if request.method == "POST":
        form = BlogPostForm(
            request.POST,
            request.FILES,
            instance=post # Without instance=post, Django would create an empty form instead
        )

        if form.is_valid():
            form.save() # Django updates that existing database record rather than creating a new post
            messages.success(request, "Blog post updated successfully.")
            return redirect(post.get_absolute_url())
    else:
        form = BlogPostForm(instance=post)

    return render(request, "post_form.html", {
        "form": form,
        "title": "Edit Blog Post"
    })


@login_required
def post_delete(request, pk):
    post = get_object_or_404(
        BlogPost,
        pk=pk,
        author=request.user
    )

    if request.method == "POST":
        post.delete()
        messages.success(request, "Blog post deleted successfully.")
        return redirect("home")

    return render(request, "post_confirm_delete.html", {
        "post": post
    })


def signup(request):
    if request.user.is_authenticated:
        return redirect("home")

    if request.method == "POST":
        form = SignUpForm(request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user) # This logs in the newly registered user by establishing their authenticated session
            messages.success(request, "Your account has been created.")
            return redirect("home")
    else:
        form = SignUpForm()

    return render(request, "registration/signup.html", {
        "form": form
    })