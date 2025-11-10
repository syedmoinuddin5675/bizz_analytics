from django.db import models

class Sale(models.Model):
    date = models.DateField(null=True, blank=True)   # ✅ date optional bana diya
    product = models.CharField(max_length=100)
    category = models.CharField(max_length=100, default="General")
    amount = models.FloatField()

    def __str__(self):
        return f"{self.product} - {self.amount}"
