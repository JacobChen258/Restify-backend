from django.contrib import admin
from .models import Restaurant,Restaurant_Like,Images

# Register your models here.

admin.site.register(Restaurant)
admin.site.register(Restaurant_Like)
admin.site.register(Images)