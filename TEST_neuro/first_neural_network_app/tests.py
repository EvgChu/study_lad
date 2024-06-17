from django.test import TestCase
from .models import Layer
import numpy as np
import pickle


class LayerModelTests(TestCase):

    def test_save_array_to_blob(self):
        layer = Layer(name='Layer for tests')
        layer.save()

        weights_array = np.array([0.5, 0.48, -0.7])
        layer.alpha = 0.1
        layer.number_of_iterations = 40
        layer.save_array_to_blob(weights_array)

        saved_layer = Layer.objects.get(id=layer.id)
        serialized_data = saved_layer.weights
        self.assertEqual(pickle.loads(serialized_data).tolist(), weights_array.tolist())

        layer.calculate_loss(None, None)

