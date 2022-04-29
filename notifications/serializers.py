from rest_framework.serializers import ModelSerializer
from notifications.models import Notification

class NotificationsSerializer(ModelSerializer):

    class Meta:
        model = Notification
        fields = ['viewer','content']

class GetNotificationsSerializer(ModelSerializer):

    class Meta:
        model = Notification
        fields = ['id','content']