from django.http import Http404
from django.shortcuts import get_object_or_404

from blogs.serializers.blog import BlogSerializer
from pagination import TinyResultsSetPagination
from blogs.models import Blog

from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from restaurants.models import Restaurant

class RestaurantBlogs(ListAPIView):
    serializer_class = BlogSerializer
    pagination_class = TinyResultsSetPagination

    def get_queryset(self):
        res = get_object_or_404(Restaurant,id=self.kwargs['res_id'])

        return Blog.objects.filter(restaurant=res.id).order_by('id')
