from django.shortcuts import get_object_or_404
from rest_framework.generics import DestroyAPIView,ListAPIView
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated
from notifications.models import Notification
from notifications.serializers import GetNotificationsSerializer
from pagination import TinyResultsSetPagination
from rest_framework.response import Response
from rest_framework import status

class NotificationView(DestroyAPIView,ListAPIView):
    serializer_class = GetNotificationsSerializer
    permission_classes = [IsAuthenticated,]
    pagination_class = TinyResultsSetPagination
    
    def get_queryset(self):
        user = self.request.user
        return Notification.objects.filter(viewer=user.id).order_by('-creation_time')

    def delete(self, request, *args, **kwargs):
        if 'notif_id' not in self.request.data:
            return Response(status=status.HTTP_400_BAD_REQUEST,data={'detail':'missing notification id'})
        return super().delete(request, *args, **kwargs)

    def get_object(self):
        notif = get_object_or_404(Notification,id=self.request.data["notif_id"])
        if notif.viewer.id != self.request.user.id:
            raise PermissionDenied
        return notif

class DeleteAllNotifView(DestroyAPIView):
    permission_classes = [IsAuthenticated,]

    def destroy(self, request, *args, **kwargs):
        instances = self.get_queryset()
        for instance in instances:
            self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def get_queryset(self):
        user=self.request.user
        return Notification.objects.filter(viewer=user.id)

    def perform_destroy(self, instance):
        instance.delete()
    