from django.urls import path
from .views import CommentView

app_name = "comments"

urlpatterns = [
    path("create/",CommentView.as_view(),name="create_comment"),
    path("<int:res_id>/",CommentView.as_view(),name="restaurant_comments"),
]