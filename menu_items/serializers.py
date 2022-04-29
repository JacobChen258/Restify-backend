from rest_framework import serializers
from menu_items.models import MenuItem

class MenuItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = MenuItem
        fields = ['id', 'name', 'description', 'price', 'restaurant']

