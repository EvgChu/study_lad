from django.shortcuts import render

def index(request):
    return render(request, 'first_neural_network_app/index.html')