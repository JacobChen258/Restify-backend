from django.urls import path
from notifications.views import NotificationView
from notifications.views import DeleteAllNotifView

app_name = "notifications"

urlpatterns = [
    path("",NotificationView.as_view(),name="notifications"),
    path("delete_all/",DeleteAllNotifView.as_view(),name="del_notifications")
]