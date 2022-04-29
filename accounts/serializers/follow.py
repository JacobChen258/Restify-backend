from rest_framework import serializers
from ..models import FollowedRestaurant

class FollowedRestaurantSerializer(serializers.ModelSerializer):
    class Meta:
        model = FollowedRestaurant
        fields = ['id', 'restaurant', 'user']

