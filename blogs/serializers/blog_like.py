from rest_framework import serializers
from blogs.models import Blog_Likes

class LikedBlogSerializer(serializers.ModelSerializer):
    class Meta:
        model = Blog_Likes
        fields = ['id', 'user', 'blog']