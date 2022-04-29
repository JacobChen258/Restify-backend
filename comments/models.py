from django.db import models
from django.db.models.deletion import CASCADE


# Create your models here.
class Comment(models.Model):
    user = models.ForeignKey(to='accounts.User',on_delete=CASCADE,null=False, blank=False)
    restaurant = models.ForeignKey(to='restaurants.Restaurant',on_delete=CASCADE,null=False, blank=False)
    content = models.CharField(max_length=300,null=False,blank=False)
    creation_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username + "_"+ self.restaurant.name
