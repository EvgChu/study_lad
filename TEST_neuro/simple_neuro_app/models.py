from django.db import models

class Neuron(models.Model):
    class VERSION_CHOICES(models.TextChoices):
        V1 = '1'

    title = models.CharField(max_length=200)
    weight = models.FloatField()
    step_amount = models.FloatField()
    goal_prediction = models.FloatField()
    number_of_iterations  = models.IntegerField()
    version = models.CharField(
        max_length=20, 
        choices=VERSION_CHOICES.choices, 
        default=VERSION_CHOICES.V1
    )

    def __str__(self):
        return f"{self.title} (v{self.version}), w={self.weight}, s={self.step_amount}, N={self.number_of_iterations}"

    def calculate(self, input_data):
        if self.version == Neuron.VERSION_CHOICES.V1:
            return self._calculate_v1(input_data)
        else:
            raise ValueError(f"Unknown version: {self.version}")
        
    def _calculate_v1(self, input_value):
        input_value = float(input_value)
        msgs = []
        weight = self.weight
        for i in range(self.number_of_iterations):
            prediction = input_value * weight
            error = (prediction - self.goal_prediction) ** 2
            msgs.append(f'№{i}) Error: {error}, Prediction: {prediction}, Weight: {weight}')

            up_prediction = input_value * (weight + self.step_amount)
            up_error = (self.goal_prediction - up_prediction)  **  2

            down_prediction = input_value * (weight  - self.step_amount)
            down_error  =  (self.goal_prediction - down_prediction)  **  2

            if down_error < up_error:
                weight = weight - self.step_amount
                self.save()
            elif down_error > up_error:
                weight = weight - self.step_amount

        self.save()

        return msgs