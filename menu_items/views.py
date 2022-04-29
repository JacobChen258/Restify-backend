from django.http import Http404
from django.shortcuts import get_object_or_404

from menu_items.serializers import MenuItemSerializer
from menu_items.models import MenuItem
from rest_framework.generics import ListAPIView,DestroyAPIView,CreateAPIView,UpdateAPIView
from rest_framework.permissions import IsAuthenticated
from pagination import ItemResultSetPagination
from restaurants.models import Restaurant
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response
from rest_framework import status
from notifications.serializers import NotificationsSerializer
from accounts.models import FollowedRestaurant
from rest_framework.status import HTTP_200_OK

class MenuItemView(DestroyAPIView,UpdateAPIView,CreateAPIView,ListAPIView):
    serializer_class = MenuItemSerializer
    pagination_class = ItemResultSetPagination

    def get_queryset(self):
        self.permission_classes = []
        res = get_object_or_404(Restaurant,id=self.kwargs['res_id'])
        menu = MenuItem.objects.filter(restaurant=res.id).order_by('id')

        return menu

    def get_object(self):
        res = get_object_or_404(Restaurant,owner=self.request.user.id)
        item = get_object_or_404(MenuItem,id=self.kwargs["item_id"])
        if item.restaurant.id != res.id:
            raise PermissionDenied
        return item

    def update(self, request, *args, **kwargs):
        self.permission_classes = [IsAuthenticated,]
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data,partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        restaurant = get_object_or_404(Restaurant, owner=request.user.id)
        self.restaurant = restaurant
        self.notify_users()

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        self.permission_classes = [IsAuthenticated,]
        data = self.request.data.copy()
        self.restaurant = get_object_or_404(Restaurant,owner=self.request.user.id)
        data['restaurant'] = get_object_or_404(Restaurant,owner=self.request.user.id).id
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        self.notify_users()
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def notify_users(self):
        records = FollowedRestaurant.objects.filter(restaurant=self.restaurant.id)
        content = f"The restaurant {self.restaurant.name} you followed just added a new item."
        data_lst = [{'viewer':record.user.id,'content':content} for record in records]
        notif_serializer = NotificationsSerializer(data=data_lst,many=True)
        notif_serializer.is_valid(raise_exception=True)
        notif_serializer.save()
