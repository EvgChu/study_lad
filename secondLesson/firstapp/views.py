from django.http import HttpResponse

def index(request):
    return HttpResponse("Hello World")

def about(request):
    return HttpResponse("Hello World")

def producut(request, productId=0):
    output = f"productId {productId}"
    return HttpResponse(output)

def user(request, id, name):
    output = f"ID {id}, NAME {name}"
    return HttpResponse(output)