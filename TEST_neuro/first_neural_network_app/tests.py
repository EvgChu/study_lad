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
        self.layer.save_weights_to_blob(self.weights)

    def test_save_and_load_array_to_blob(self):
        loaded_weights = self.layer.load_weights_from_blob()
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
        
        self.layer_mid.save_weights_to_blob(self.weights_0_1)

        self.layer_out.previous_layer = self.layer_mid
        self.layer_out.save_weights_to_blob(self.weights_1_2)

        self.neuronet = NeuroNet.objects.create(
            name="Test Network",
            first_layer=self.layer_mid,
            last_layer=self.layer_out,
            number_of_layers=2
        )


    def test_compare_example_from_book(self):

        def relu(x):
            return np.maximum(0, x)
        
        def relu2deriv(output):
            return output > 0
        
        walk_vs_stop = np.array([[1,  1,  0,  0]]).T
 
        for iteration in range(10):
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

                self.weights_1_2 -= self.alpha * layer_1.T.dot(layer_2_delta)
                self.weights_0_1 -= self.alpha * layer_0.T.dot(layer_1_delta)

                self.neuronet.update_weights(activations, deltas)

                np.testing.assert_almost_equal(self.layer_out.load_weights_from_blob(), self.weights_1_2)
                np.testing.assert_almost_equal(self.layer_mid.load_weights_from_blob(), self.weights_0_1)

            if iteration % 10 == 9:
                print("Iteration: ", iteration, "Error: ", layer_2_error)

    def test_example_image_with_kernel(self):
        np.random.seed(1)
        from keras.datasets import mnist

        (x_train, y_train), (x_test, y_test) = mnist.load_data()

        images , labels  = x_train[0:1000].reshape(1000, 28*28) / 255, y_train[0:1000]

        one_hot_labels = np.zeros((len(labels), 10))

        for i, l in enumerate(labels):
            one_hot_labels[i, l] = 1

        labels = one_hot_labels

        test_images = x_test.reshape(len(x_test), 28*28) / 255
        test_labels = np.zeros((len(y_test), 10))

        for i, l in enumerate(y_test):
            test_labels[i, l]  =  1

        def tanh(x):
            return np.tanh(x)

        def tanh2deriv(output):
            return 1 - (output ** 2)
        
        def softmax(x):
            temp = np.exp(x)
            return temp /  np.sum(temp, axis=1, keepdims=True)
        
        alpha, iteration = (2, 1)

        pixels_per_image, num_labels = (784, 10)

        batch_size = 128
        input_rows = 28
        input_cols = 28

        kernel_rows = 3
        kernel_cols = 3

        num_kernels = 16

        hidden_size = ((input_rows - kernel_rows) * (input_cols - kernel_cols)) * num_kernels
        kernels = 0.02 * np.random.random((kernel_rows*kernel_cols, num_kernels)) - 0.01

        weights_1_2 = 0.2 * np.random.random((hidden_size,  num_labels)) - 0.1

        def get_image_section(layer, row_from,row_to, col_from, col_to):
            section = layer[:,row_from:row_to, col_from:col_to]
            return section.reshape(-1, 1, row_to-row_from, col_to-col_from)
        
        for j in range(iteration):
            correct_cnt = 0
            for i in range(len(images) // batch_size):
                batch_start = i * batch_size
                batch_end = (i + 1) * batch_size
                layer_0 = images[batch_start:batch_end]
                layer_0 = layer_0.reshape(layer_0.shape[0], 28, 28)
                layer_0.shape

                sects = list()

                for row_start in range(layer_0.shape[1] - kernel_rows):
                    for col_start in range(layer_0.shape[2] - kernel_cols):
                        sect= get_image_section(
                            layer_0, 
                            row_start, 
                            row_start + kernel_rows, 
                            col_start, 
                            col_start + kernel_cols
                        )
                        sects.append(sect)

                expanded_input = np.concatenate(sects, axis=1)
                es = expanded_input.shape
                flattened_input  = expanded_input.reshape(es[0]*es[1], -1)

                kernel_output = flattened_input.dot(kernels)
                layer_1 = tanh(kernel_output.reshape(es[0], -1))

                dropout_mask = np.random.randint(2, size=layer_1.shape)

                layer_1 *= dropout_mask * 2

                layer_2 = softmax(np.dot(layer_1, weights_1_2))

                for k in range(batch_size):
                    labelset = labels[batch_start + k: batch_start + k + 1]
                    _inc = int(np.argmax(layer_2[k:k+1]) == np.argmax(labelset))
                    correct_cnt += _inc

                layer_2_delta = (labels[batch_start:batch_end] - layer_2) / (batch_size * layer_2.shape[0])
                layer_1_delta = layer_2_delta.dot(weights_1_2.T) * tanh2deriv(layer_1)
                layer_1_delta *=  dropout_mask

                weights_1_2 += alpha * layer_1.T.dot(layer_2_delta)
                l1d_reshape = layer_1_delta.reshape(kernel_output.shape)
                k_update = flattened_input.T.dot(l1d_reshape)
                kernels -= alpha * k_update

            test_correct_cnt = 0

            for i in range(len(test_images)):
                layer_0 = test_images[i:i+1]
                layer_0 = layer_0.reshape(layer_0.shape[0],  28,  28)
                layer_0.shape

                sects  = list()
                for row_start in range(layer_0.shape[1] - kernel_rows):
                    for col_start in range(layer_0.shape[2] - kernel_cols):
                        sect= get_image_section(
                            layer_0, 
                            row_start, 
                            row_start + kernel_rows, 
                            col_start, 
                            col_start + kernel_cols
                        )
                        sects.append(sect)
                expanded_input = np.concatenate(sects, axis=1)
                es = expanded_input.shape

                flattened_input = expanded_input.reshape(es[0]*es[1],  -1)

                kernel_output = flattened_input.dot(kernels)
                layer_1 = tanh(kernel_output.reshape(es[0],  -1))
                layer_2 = np.dot(layer_1, weights_1_2)

                test_correct_cnt += int(np.argmax(layer_2) == np.argmax(test_labels[i:i+1]))

            if j % 1 == 0:
                print(
                    f"I: {j} Test-Acc: {test_correct_cnt / len(test_images)} "
                    f"Train-Acc: {correct_cnt / len(images)}"
                )

