from django.http import (
    HttpResponse,
    HttpResponsePermanentRedirect,
    HttpResponseRedirect,
    HttpResponseBadRequest,
    HttpResponseForbidden
    )

from django.shortcuts import render

def index(request):

    return render(request, "firstapp/index.html")
    return HttpResponsePermanentRedirect("/about/")
    return HttpResponseRedirect("/about/")
    return HttpResponse("Hello World")

def about(request):
    return HttpResponse("about")

def producut(request, productId=0):
    category = request.GET.get("cat", "Not define")
    output = f"productId №{productId}, category: {category}"
    return HttpResponse(output)

def user(request):
    id = request.GET.get("id", "Not define")
    name = request.GET.get("name", "Not define")
    output = f"<p>ID {id}</p><p> NAME {name}</p>"
    return HttpResponse(output)

def access(request, age):
    if age not in range(1, 111):
        return HttpResponseBadRequest("Enter correct data")
    if age > 17:
        return HttpResponse("Access open")
    else:
        return HttpResponseForbidden("Access block, only for adults")
    