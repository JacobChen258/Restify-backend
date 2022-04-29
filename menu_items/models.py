from django.db import models
from django.db.models.deletion import CASCADE
from restaurants.models import Restaurant
# Create your models here.
class MenuItem(models.Model):
    name = models.CharField(max_length=80,null=False, blank=False)
    description = models.TextField(max_length=500)
    price = models.DecimalField(max_digits=8, decimal_places=2,null=False, blank=False)
    restaurant = models.ForeignKey(to=Restaurant, on_delete=CASCADE,null=False, blank=False)

    class Meta:
        unique_together = ('name', 'restaurant',)

    def __str__(self):
        return self.name