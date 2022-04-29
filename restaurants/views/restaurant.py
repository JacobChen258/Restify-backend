from ..serializers import CreateRestaurantSerializer,EditRestaurantSerializer,RestaurantInfoSerializer
from rest_framework.generics import CreateAPIView,UpdateAPIView
from restaurants.models import Restaurant
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.status import HTTP_200_OK
from django.shortcuts import get_object_or_404
from rest_framework.generics import RetrieveAPIView


class RestaurantView(CreateAPIView,UpdateAPIView,RetrieveAPIView):
    serializer_class = CreateRestaurantSerializer

    def post(self, request, *args, **kwargs):
        self.serializer_class = CreateRestaurantSerializer
        self.permission_classes = [IsAuthenticated,]
        return self.create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        self.permission_classes = [IsAuthenticated,]
        partial = kwargs.pop('partial', False)
        self.serializer_class = EditRestaurantSerializer
        instance = get_object_or_404(Restaurant,owner = request.user)
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        data = request.data.copy()
        data['owner'] = request.user.id
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        restaurant = Restaurant.objects.filter(owner=self.request.user.id)
        return Response({"id":restaurant[0].id}, status=status.HTTP_201_CREATED, headers=headers)
    
    def get(self, request, *args, **kwargs):
        self.permission_classes = []
        self.serializer_class = RestaurantInfoSerializer
        return super().get(request, *args, **kwargs)
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
        
    def get_object(self):
        return get_object_or_404(Restaurant,id=self.kwargs['res_id'])
