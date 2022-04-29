from django.shortcuts import get_object_or_404
from rest_framework.generics import ListAPIView,CreateAPIView
from comments.serializers import RestaurantCommentSerializer,AddCommentSerializer
from rest_framework.permissions import IsAuthenticated
from comments.models import Comment
from pagination import CommentResultSetPagination
from restaurants.models import Restaurant
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED
from notifications.serializers import NotificationsSerializer
from accounts.models import User

class CommentView(ListAPIView,CreateAPIView):
    pagination_class = CommentResultSetPagination
    
    def get(self, request, *args, **kwargs):
        self.permission_classes = []
        self.serializer_class = RestaurantCommentSerializer
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        restaurant = get_object_or_404(Restaurant, id=self.kwargs['res_id'])
        return Comment.objects.filter(restaurant=restaurant).order_by('-creation_time')

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            data = self.get_user_name(serializer_data=serializer.data)
            return self.get_paginated_response(data)
        serializer = self.get_serializer(queryset, many=True)
        data = self.get_user_name(serializer_data=serializer.data)
        return Response(data)

    def post(self, request, *args, **kwargs):
        self.permission_classes = [IsAuthenticated,]
        self.serializer_class = AddCommentSerializer
        return self.create(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        data = request.data.copy()
        data["user"] = request.user.id
        self.object = get_object_or_404(Restaurant,id=self.request.data['restaurant'])
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        self.notify_owner()
        headers = self.get_success_headers(serializer.data)
        data = serializer.data
        data['full_name'] = request.user.first_name +" "+ request.user.last_name
        return Response(data, status=HTTP_201_CREATED, headers=headers)

    def notify_owner(self):
        owner = User.objects.filter(id=self.object.owner.id)[0]
        data = {
            'viewer': owner.id,
            'content': f"{self.request.user.username} just commented on your restaurant."

        }
        notify_serializer = NotificationsSerializer(data=data)
        notify_serializer.is_valid(raise_exception=True)
        notify_serializer.save()

    def get_user_name(self,serializer_data):
        dataset = serializer_data
        for data in dataset:
            user = get_object_or_404(User,id=data['user'])
            data['full_name'] = user.first_name + " "+ user.last_name
            data.pop('user')
        return dataset
        

            