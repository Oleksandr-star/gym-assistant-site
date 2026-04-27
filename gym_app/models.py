from django.db import models
from django.contrib.auth.models import User

class Exercise(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='exercises')
    name = models.CharField(max_length=100)
    weight = models.FloatField()
    reps = models.IntegerField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.date.strftime('%d.%m.%Y')})"

class WeightRecord(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='weight_records')
    weight = models.FloatField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.weight} кг ({self.date.strftime('%d.%m.%Y')})"