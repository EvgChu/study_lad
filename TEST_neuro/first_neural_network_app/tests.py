from django.test import TestCase
from .models import NeuroNet, Layer
import numpy as np
import pickle

class LayerTestCase(TestCase):
    
    def setUp(self):
        self.layer = Layer.objects.create(
            name="Test Layer",
            alpha=0.01,
            type_fn_activation='relu'
        )
        self.weights = np.array([[0.2, 0.8], [0.6, 0.4]])
        self.layer.save_array_to_blob(self.weights)

    def test_save_and_load_array_to_blob(self):
        loaded_weights = self.layer.load_array_from_blob()
        np.testing.assert_array_equal(self.weights, loaded_weights)

    def test_activation_functions(self):
        x = np.array([-1, 0, 1])
        np.testing.assert_array_equal(self.layer._relu(x), np.array([0, 0, 1]))
        self.layer.type_fn_activation = 'sigmoid'
        self.layer.save()
        np.testing.assert_almost_equal(self.layer._sigmoid(x), np.array([0.26894142, 0.5, 0.73105858]), decimal=5)
        self.layer.type_fn_activation = 'tanh'
        self.layer.save()
        np.testing.assert_almost_equal(self.layer._tanh(x), np.array([-0.76159416, 0., 0.76159416]), decimal=5)

    def test_activation_derivative_functions(self):
        output = np.array([0, 1])
        np.testing.assert_array_equal(self.layer._relu2deriv(output), np.array([0, 1]))
        self.layer.type_fn_activation = 'none'
        self.layer.save()
        np.testing.assert_array_equal(self.layer.activate_deriv(output), output)



class NeuroNetTestCase(TestCase):
    def setUp(self):

        self.streetlights = np.array([
            [1,  0,  1],
            [0,  1,  1],
            [0,  0,  1],
            [1,  1,  1]
        ])


        self.hidden_size = 4
        self.alpha = 0.2

        self.layer_out = Layer.objects.create(
            name="Layer 2",
            alpha=self.alpha,
            type_fn_activation='none'
        )
        self.layer_mid = Layer.objects.create(
            name="Layer 1",
            next_layer=self.layer_out,
            alpha=self.alpha,
            type_fn_activation='relu'
        )
        self.weights_0_1 = 2*np.random.random((3,  self.hidden_size)) - 1
        self.weights_1_2 = 2*np.random.random((self.hidden_size,  1)) - 1      
        
        self.layer_mid.save_array_to_blob(self.weights_0_1)

        self.layer_out.previous_layer = self.layer_mid
        self.layer_out.save_array_to_blob(self.weights_1_2)

        self.neuronet = NeuroNet.objects.create(
            name="Test Network",
            first_layer=self.layer_mid,
            last_layer=self.layer_out,
            number_of_layers=2
        )


    def test_compare_example_from_book(self):
        np.random.seed(1)

        def relu(x):
            return np.maximum(0, x)
        
        def relu2deriv(output):
            return output > 0
        
        walk_vs_stop = np.array([[1,  1,  0,  0]]).T

        alpha = self.alpha

        print()
        for iteration in range(200):
            layer_2_error = 0
            for i in range(len(self.streetlights)):
                layer_0 =  self.streetlights[i:i+1]
                layer_1 = relu(np.dot(layer_0, self.weights_0_1))
                layer_2 = np.dot(layer_1, self.weights_1_2)

                activations = self.neuronet.forward_propagate(self.streetlights[i:i+1])   
                np.testing.assert_almost_equal(activations[0], layer_0)
                np.testing.assert_almost_equal(activations[1], layer_1)
                np.testing.assert_almost_equal(activations[2], layer_2)

                layer_2_error += np.sum((layer_2 - walk_vs_stop[i:i+1]) ** 2)

                layer_2_delta = (layer_2  - walk_vs_stop[i:i+1])
                layer_1_delta  = layer_2_delta.dot(self.weights_1_2.T) * relu2deriv(layer_1)
        
                deltas = self.neuronet.back_propagate(activations, walk_vs_stop[i:i+1])

                np.testing.assert_almost_equal(deltas[1], layer_2_delta)
                np.testing.assert_almost_equal(deltas[0], layer_1_delta)

                self.weights_1_2 -= alpha * layer_1.T.dot(layer_2_delta)
                self.weights_0_1 -= alpha * layer_0.T.dot(layer_1_delta)

                self.neuronet.update_weights(activations, deltas)

                np.testing.assert_almost_equal(self.layer_out.load_array_from_blob(), self.weights_1_2)
                np.testing.assert_almost_equal(self.layer_mid.load_array_from_blob(), self.weights_0_1)

            if iteration % 10 == 9:
                print("Iteration: ", iteration, "Error: ", layer_2_error)

