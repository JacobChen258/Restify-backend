from django.db import models
from django.db.models.deletion import CASCADE
# Create your models here
class Restaurant(models.Model):
    owner = models.OneToOneField(to='accounts.User', on_delete=CASCADE, null=False, blank=False)
    name = models.CharField(null=False, blank=False,max_length=100)
    address = models.CharField(null=False, blank=False,max_length=100)  
    logo = models.ImageField(upload_to='logos/',default='avatars/user-default.jpeg')
    email = models.EmailField(null=False, blank=False)
    postal_code = models.CharField(null=False, blank=False,max_length=10)
    phone_num = models.CharField(null=False, blank=False,max_length=20)  
    num_followers = models.PositiveIntegerField(default=0)
    num_likes = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.name

class Restaurant_Like(models.Model):
    user = models.ForeignKey(to='accounts.User', on_delete=models.DO_NOTHING,null=False, blank=False)
    restaurant = models.ForeignKey(to=Restaurant, on_delete=models.CASCADE,null=False, blank=False)

    class Meta:
        unique_together = ('user', 'restaurant',)

    def __str__(self):
        return self.user.username +"_"+ self.restaurant.name
        
class Images(models.Model):
    restaurant = models.ForeignKey(to=Restaurant,on_delete=CASCADE,null=False, blank=False)
    image = models.ImageField(upload_to = "item_images/",null=False, blank=False)  
    creation_time = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.image.url