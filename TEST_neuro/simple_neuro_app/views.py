from django.shortcuts import render
from .models import Neuron
from .forms import NeuronForm, InputDataFrom
from django.shortcuts import render, get_object_or_404, redirect


def index(request):
    neurons = Neuron.objects.all()
    return render(request, 'simple_neuro_app/index.html', {'neurons': neurons})


def add_neuron(request):
    form = NeuronForm()
    if request.method == 'POST':
        form = NeuronForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(request, 'index')
    return render(request, 'simple_neuro_app/add_neuron.html', {'form': form})


def neuron_edit(request, pk): 
    neuron = get_object_or_404(Neuron, pk=pk)
    if request.method == 'POST':
        form = NeuronForm(request.POST, instance=neuron)
        if form.is_valid():
            form.save()
            return redirect('calculate', neuron.pk)
    else:
        form = NeuronForm(instance=neuron)
    return render(request, 'simple_neuro_app/add_neuron.html', {'form': form})


def calculate(request, pk): 
    neuron = get_object_or_404(Neuron, pk=pk)
    msgs = []
    form = InputDataFrom(request.POST) 
    if request.method == 'POST':
        try:
            if form.is_valid():
                input_value = form.cleaned_data['input_data']
                res = neuron.calculate(input_value) 
                msgs.extend(res)
        except Exception as e:
            msgs.append(f'Error: {e}')

    return render(request, 'simple_neuro_app/show_result.html', {'form': form, 'msgs': msgs, 'neuron': neuron})
 