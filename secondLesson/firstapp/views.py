from django.http import HttpResponse

def index(request):
    return HttpResponse("Hello World")

def about(request):
    return HttpResponse("Hello World")

def producut(request, productId=0):
    category = request.GET.get("cat", "Not define")
    output = f"productId №{productId}, category: {category}"
    return HttpResponse(output)

def user(request):
    id = request.GET.get("id", "Not define")
    name = request.GET.get("name", "Not define")
    output = f"<p>ID {id}</p><p> NAME {name}</p>"
    return HttpResponse(output)