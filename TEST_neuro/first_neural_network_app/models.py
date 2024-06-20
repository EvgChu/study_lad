from django.db import models
import pickle
import numpy as np

class Layer(models.Model):
    name = models.CharField(max_length=255)
    weights = models.BinaryField()
    size = models.IntegerField(default=0)
    next_layer = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='_previous_layers')
    previous_layer = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='_next_layers')
    alpha = models.FloatField(default=1)
    type_fn_activation = models.CharField(max_length=255, choices=[
        ('none', 'None'),
        ('relu', 'ReLU'),
        ('sigmoid', 'Sigmoid'),
        ('tanh', 'Tanh')
    ], default='relu')
  
    def _relu(self, x):
        return (x > 0) * x

    def _relu2deriv(self, output):
        return output > 0

    def _sigmoid(self, x):
        return 1 / (1 + np.exp(-x))

    def _sigmoid2deriv(self, output):
        raise NotImplementedError

    def _tanh(self, x):
        return np.tanh(x)

    def _tanh2deriv(self, output):
        raise NotImplementedError

    def activate(self, x):
        if self.type_fn_activation == 'none':
            return x
        elif self.type_fn_activation == 'relu':
            return self._relu(x)
        elif self.type_fn_activation == 'sigmoid':
            return self._sigmoid(x)
        elif self.type_fn_activation == 'tanh':
            return self._tanh(x)
        else:
            raise ValueError("Unknown activation function")

    def activate_deriv(self, output):
        if self.type_fn_activation == 'none':
            return output
        elif self.type_fn_activation == 'relu':
            return self._relu2deriv(output)
        elif self.type_fn_activation == 'sigmoid':
            return self._sigmoid2deriv(output)
        elif self.type_fn_activation == 'tanh':
            return self._tanh2deriv(output)
        else:
            raise ValueError("Unknown activation function")

    def save_array_to_blob(self, data_array): 
        serialized_data = pickle.dumps(data_array) 
        self.weights = serialized_data
        self.size  = len(data_array)
        self.save()

    def load_array_from_blob(self): 
        serialized_data = self.weights 
        data_array = pickle.loads(serialized_data)
        return data_array


class NeuroNet(models.Model):
    name  = models.CharField(max_length=255)
    first_layer  = models.ForeignKey(Layer, null=True, blank=True, on_delete=models.SET_NULL, related_name='first_layer')
    last_layer   = models.ForeignKey(Layer, null=True, blank=True, on_delete=models.SET_NULL, related_name='last_layer')
    number_of_layers = models.IntegerField()

    def __str__(self):
        return self.name

    def forward_propagate(self, input_data):
        current_layer = self.first_layer
        activations = [input_data]
        while current_layer:
            weights = current_layer.load_array_from_blob()
            input_data = current_layer.activate(np.dot(input_data, weights))
            activations.append(input_data)
            current_layer = current_layer.next_layer
        return activations

    def back_propagate(self, activations, goal_arr):
  
        current_layer = self.last_layer
        deltas = [current_layer.activate_deriv(activations[-1] - goal_arr)]
        layer_index = -2
        while current_layer.previous_layer:
            error = deltas[-1].dot(current_layer.load_array_from_blob().T)
            current_layer = current_layer.previous_layer
            delta = error * current_layer.activate_deriv(activations[layer_index])
            deltas.append(delta)
            layer_index -= 1

        deltas.reverse()

        return deltas

    def update_weights(self, activations, deltas):
        current_layer = self.first_layer
        for i in range(len(deltas)):
            layer_input = np.atleast_2d(activations[i])
            delta = np.atleast_2d(deltas[i])
            current_weights = current_layer.load_array_from_blob()
            current_weights -= current_layer.alpha * layer_input.T.dot(delta)
            current_layer.save_array_to_blob(current_weights)
            current_layer = current_layer.next_layer

    def education(self, input_arr, goal_arr, epochs=10000):
        for epoch in range(epochs):
            activations = self.forward_propagate(input_arr)
            deltas = self.back_propagate(activations, goal_arr)
            self.update_weights(activations, deltas)
