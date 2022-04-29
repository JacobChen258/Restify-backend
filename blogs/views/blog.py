from rest_framework.generics import get_object_or_404
from blogs.serializers.blog import BlogSerializer
from restaurants.models import Restaurant
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import DestroyAPIView
from rest_framework.exceptions import PermissionDenied
from blogs.models import Blog
from rest_framework.generics import RetrieveAPIView
from rest_framework.status import HTTP_400_BAD_REQUEST

class Blogs(DestroyAPIView,RetrieveAPIView):
    serializer_class = BlogSerializer

    def get(self, request, *args, **kwargs):
        self.permission_classes = []
        if "blog_id" not in self.kwargs:
            return Response(status = HTTP_400_BAD_REQUEST,data={'detail':"missing blog id"})
        return super().get(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        data = serializer.data
        data['res_name'] = Restaurant.objects.filter(id=data['restaurant'])[0].name
        return Response(data)

    def get_object(self):
        blog = get_object_or_404(Blog, id=self.kwargs["blog_id"])
        return blog

    def delete(self, request, *args, **kwargs):
        self.permission_classes = [IsAuthenticated,]
        if "blog_id" not in self.kwargs:
            return Response(status=HTTP_400_BAD_REQUEST,data={'detail':"missing blog id"})
        if not (self.request.user.id):
            return Response(status=status.HTTP_401_UNAUTHORIZED,data={'detail':"please login"})
        blog = get_object_or_404(Blog, id=self.kwargs['blog_id'])
        restaurant = Restaurant.objects.filter(owner=self.request.user.id)
        if len(Restaurant.objects.filter(owner=self.request.user.id)) == 0:
            return Response(status=status.HTTP_403_FORBIDDEN,data={'detail':"you cannot delete this blog"})
        restaurant = restaurant[0]
        if blog.restaurant.id == restaurant.id:
            self.perform_destroy(blog)
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(stauts=status.HTTP_403_FORBIDDEN,data={'detail':"you cannot delete this blog"})
