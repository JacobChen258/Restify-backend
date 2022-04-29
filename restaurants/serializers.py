from rest_framework.serializers import ModelSerializer,ValidationError
from restaurants.models import Restaurant,Images,Restaurant_Like

class CreateRestaurantSerializer(ModelSerializer):
    class Meta:
        model = Restaurant
        fields = ['owner', 'name', 'address', 'logo', 'email', 'postal_code', 'phone_num']

class EditRestaurantSerializer(ModelSerializer):
    class Meta:
        model = Restaurant
        fields = ['name', 'address', 'logo', 'email', 'postal_code', 'phone_num']


class RestaurantInfoSerializer(ModelSerializer):

    class Meta:
        model = Restaurant
        fields = ['id','name', 'address', 'logo', 'email', 'postal_code', 'phone_num', 'num_followers', 'num_likes']

class AddImageSerializer(ModelSerializer):
    class Meta:
        model = Images
        fields = ['restaurant','image']

class GetImageSerializer(ModelSerializer):
    class Meta:
        model = Images
        fields = ['id','image']

class RestaurantSearchSerializer(ModelSerializer):
    class Meta:
        model = Restaurant
        fields = ['id','name','logo','num_likes','num_followers']

class LikedRestaurantSerializer(ModelSerializer):
    class Meta:
        model = Restaurant_Like
        fields = ['id', 'user', 'restaurant']