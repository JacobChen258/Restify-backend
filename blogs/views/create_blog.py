from django.shortcuts import get_object_or_404

from blogs.serializers.blog import BlogSerializer
from rest_framework.permissions import IsAuthenticated
from restaurants.models import Restaurant
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated
from notifications.serializers import NotificationsSerializer
from accounts.models import FollowedRestaurant
from blogs.models import Blog

class AddBlog(CreateAPIView):
    serializer_class = BlogSerializer
    permission_classes = [IsAuthenticated,]

    def post(self, request, *args, **kwargs):
        restaurant = get_object_or_404(Restaurant, owner=request.user.id)
        self.object = restaurant
        return self.create(request, args, kwargs)

    def create(self, request, *args, **kwargs):
        data = request.data.copy()
        data['restaurant'] = self.object.id
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        if len(Blog.objects.filter(title=serializer.validated_data['title'],restaurant=serializer.validated_data['restaurant'])) >0:
            return Response(status=status.HTTP_409_CONFLICT,data={'detail':"cannot create two blogs with same title"})
        self.perform_create(serializer)
        self.notify_users()
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def notify_users(self):
        records = FollowedRestaurant.objects.filter(restaurant=self.object.id)
        content = f"The restaurant {self.object.name} you followed just posted a new blog."
        data_lst = [{'viewer':record.user.id,'content':content} for record in records]
        notif_serializer = NotificationsSerializer(data=data_lst,many=True)
        notif_serializer.is_valid(raise_exception=True)
        notif_serializer.save()


