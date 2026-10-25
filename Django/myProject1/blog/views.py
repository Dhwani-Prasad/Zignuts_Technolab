from django.http import HttpResponse

def home(request):
    return HttpResponse("Blog Home Page")

def about(request):
    return HttpResponse("About the Blog")

def post_detail(request, post_id):
    return HttpResponse(f"Details of Blog Post {post_id}")

def user_profile(request, username):
    return HttpResponse(f"<h1>Profile of user: {username}</h1>")

def articles_by_year(request, year):
    return HttpResponse(f"Articles from the year {year}")

# def article_detail(request, year, month):
#     return HttpResponse(f"Article Detail: Year: {year}, Month: {month}")

def article_detail(request,**kwargs):
    return HttpResponse(f"<h1> Data : {kwargs} </h1>")