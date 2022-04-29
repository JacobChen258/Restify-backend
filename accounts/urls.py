from django.urls import path

from rest_framework_simplejwt.views import (TokenObtainPairView, TokenRefreshView)

from .views.register import Register
from .views.profile import ProfileView
from .views.follow import Follow
from .views.feed import Feed
from .views.token import MyTokenObtainPairView

app_name = "accounts"

urlpatterns = [
    path("register/", Register.as_view(), name="register"),
    path("login/",MyTokenObtainPairView.as_view(),name="login"),
    path("token/refresh",TokenRefreshView.as_view(),name="token-refresh"),
    path("profile/",ProfileView.as_view(),name="profile"),
    path("follow/",Follow.as_view(),name="follow"),
    path("followed/<int:res_id>/",Follow.as_view(),name="followed"),
    path("feed/",Feed.as_view(),name="feed"),
]