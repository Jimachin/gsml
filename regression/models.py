from django.db import models

class Regression_ideal(models.Model):
    receptor_rut = models.CharField(max_length=10, primary_key=True, unique=True)
    quantity = models.PositiveIntegerField()
    date_min = models.DateTimeField(auto_now=False, auto_now_add=False)

    def __str__(self):
        return str(self.receptor_rut)