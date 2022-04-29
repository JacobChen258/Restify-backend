from django.http import Http404

from accounts.serializers.feed import FeedSerializer
from ..models import FollowedRestaurant
from blogs.models import Blog
from pagination import TinyResultsSetPagination
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from restaurants.models import Restaurant

class Feed(ListAPIView):
    serializer_class = FeedSerializer
    permission_classes = [IsAuthenticated,]
    pagination_class = TinyResultsSetPagination

    def get_queryset(self):
        feed = Blog.objects.filter(restaurant__in=FollowedRestaurant.objects.filter(user=self.request.user).values_list('restaurant', flat=True)).order_by('-num_likes').values('title', 'id','restaurant','num_likes','content')
        for item in feed:
            item['restaurant'] = Restaurant.objects.filter(id=item['restaurant'])[0]
            item['res_name'] = item['restaurant'].name
        return feed

