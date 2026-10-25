from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def home(request):
  return HttpResponse("Welcome")

def about(request):
  a = 10+20
  return HttpResponse(f"About page:  {a}")