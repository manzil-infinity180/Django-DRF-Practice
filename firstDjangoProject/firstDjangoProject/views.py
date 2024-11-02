from django.http import HttpResponse

def homepage(request):
    return HttpResponse("Hello World")


def about(request):
    return HttpResponse("Hey i am about")