from comments.models import Comment
from rest_framework.serializers import ModelSerializer

class AddCommentSerializer(ModelSerializer):

    class Meta:
        model = Comment
        fields = ['id',"user","restaurant","content",'creation_time']


class RestaurantCommentSerializer(ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id','content','user','creation_time']