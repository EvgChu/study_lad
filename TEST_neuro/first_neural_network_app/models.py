from django.db import models
import pickle
import numpy as np

class Layer(models.Model):
    name = models.CharField(max_length=255)
    weights = models.BinaryField()
    next_layer = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='previous_layers')
    alpha = models.FloatField(default=1)
    number_of_iterations = models.IntegerField(default=1)

    def save_array_to_blob(self, data_array): 
        serialized_data = pickle.dumps(data_array) 
        self.weights = serialized_data
        self.save()

    def load_array_from_blob(self): 
        serialized_data = self.weights 
        data_array = pickle.loads(serialized_data)
        return data_array
    
    def calculate_loss(self, input, goal_prediction):
        weights = self.load_array_from_blob()
        alpha = self.alpha
        streetlights = np.array(
                [[1, 0, 1],
                 [0, 1, 1],
                 [0, 0, 1],
                 [1, 1, 1],
                 [0, 1, 1],
                 [1, 0, 1]]
        )
        walk_vs_stop = np.array([ 0, 1, 0, 1, 1, 0])
        input = streetlights[0]
        goal_prediction = walk_vs_stop[0]

        for iteration in range(self.number_of_iterations):
            error_for_all_lights  = 0
            for row_index in range(len(walk_vs_stop)):
                input = streetlights[row_index]
                goal_prediction = walk_vs_stop[row_index]

                prediction = input.dot(weights)

                error = (prediction - goal_prediction) ** 2
                error_for_all_lights += error

                delta = prediction - goal_prediction
                weights = weights - (alpha * (input * delta))
                print(f"Prediction: {prediction}")
            print(f"Error:  {error_for_all_lights} \n")



