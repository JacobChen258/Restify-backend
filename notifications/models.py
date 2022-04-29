from django.db import models
from django.db.models.deletion import CASCADE
from accounts.models import User
# Create your models here.
class Notification(models.Model):
    viewer = models.ForeignKey(to=User,on_delete=CASCADE,null=False, blank=False)
    content = models.CharField(max_length=300,null=False,blank=False)
    creation_time = models.DateTimeField(auto_now_add=True)
    def __str__(self) -> str:
        return self.viewer.username + "_" + str(self.creation_time)
