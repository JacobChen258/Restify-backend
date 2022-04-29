from django.shortcuts import get_object_or_404
from rest_framework.generics import ListAPIView, DestroyAPIView, CreateAPIView
from rest_framework.permissions import IsAuthenticated
from restaurants.models import Images, Restaurant
from restaurants.serializers import GetImageSerializer, AddImageSerializer
from pagination import ImageResultSetPagination
from rest_framework.exceptions import  PermissionDenied
from restaurants.models import Restaurant,Images
from rest_framework import status
from rest_framework.response import Response

class ImageView(ListAPIView, DestroyAPIView,CreateAPIView):
    pagination_class = ImageResultSetPagination

    def get(self, request, *args, **kwargs):
        self.permission_classes = []
        self.serializer_class = GetImageSerializer
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        restaurant = get_object_or_404(Restaurant,id=self.kwargs['res_id'])
        return Images.objects.filter(restaurant=restaurant).order_by("-creation_time")

    def get_object(self):
        restaurant = get_object_or_404(Restaurant,owner = self.request.user.id)
        image = get_object_or_404(Images,id=self.request.data['image_id'])
        if image.restaurant.id == restaurant.id:
            return image
        raise PermissionDenied

    def post(self, request, *args, **kwargs):
        self.permission_classes = [IsAuthenticated,]
        self.serializer_class = AddImageSerializer
        user = request.user
        restaurant = get_object_or_404(Restaurant,owner = user.id)
        self.object = restaurant
        return self.create(request, *args, **kwargs)
    
    def create(self, request, *args, **kwargs):
        self.permission_classes = [IsAuthenticated,]
        data = request.data.copy()
        data["restaurant"] = self.object.id
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    
