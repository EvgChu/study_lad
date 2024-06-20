
from django.shortcuts import render, redirect
from .forms import NeuroNetForm, LayerForm
from .models import NeuroNet, Layer

def neuronet_list(request):
    neuronets = NeuroNet.objects.all()
    return render(request, 'first_neural_network_app/neuronet_list.html', {'neuronets': neuronets})


def create_neuronet(request):
    if request.method == 'POST':
        form = NeuroNetForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('neuronet_list') 
    else:
        form = NeuroNetForm()
    return render(request, 'first_neural_network_app/create_neuronet.html', {'form': form})


def add_layer(request, neuronet_id):
    pass

def train_neuronet(request, neuronet_id):
    pass