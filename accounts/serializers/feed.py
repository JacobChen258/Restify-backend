from rest_framework import serializers
from blogs.models import Blog
from rest_framework import fields


class FeedSerializer(serializers.ModelSerializer):
    res_name = fields.CharField()
    class Meta:
        model = Blog
        fields = ['id', 'title','restaurant','res_name','content','num_likes']

