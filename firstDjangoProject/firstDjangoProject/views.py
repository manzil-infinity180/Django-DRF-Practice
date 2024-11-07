# from django.http import HttpResponse
from django.shortcuts import render
# def homepage(request):
#     return HttpResponse("Hello World")


# def about(request):
#     return HttpResponse("Hey i am about")

def homepage(request):
    return render(request, 'homepage.html') # basically  we already setup the templates in setting.py

def about(request):
    return render(request, 'about.html')