from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.deletion import CASCADE,SET_NULL
# Create your models here.
class User(AbstractUser):
    avatar = models.ImageField(upload_to='avatars/',default='avatars/user-default.jpeg')
    phone_num = models.CharField(max_length=13,null=True,blank=True)
    def __str__(self):
        return self.username

class FollowedRestaurant(models.Model):
    restaurant = models.ForeignKey(to='restaurants.Restaurant', on_delete=CASCADE)
    user = models.ForeignKey(to=User, on_delete=CASCADE)

    class Meta:
        unique_together = ('user', 'restaurant',)

    def __str__(self):
        return self.user.username +'_'+self.restaurant.name

