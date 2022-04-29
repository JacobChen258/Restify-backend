from django.urls import path
from blogs.views.blog_like import liked_blog
from blogs.views.blog import Blogs
from blogs.views.create_blog import AddBlog
from blogs.views.restaurant_blog import RestaurantBlogs
from blogs.views.liked_blog import LikedBlog
app_name = "blogs"

urlpatterns = [
    path("like/", liked_blog, name="like_blog"),
    path("liked/<int:blog_id>/", LikedBlog.as_view(), name="liked_blog"),
    path("<int:blog_id>/",Blogs.as_view(),name="blog"),
    path("create/",AddBlog.as_view(),name='add_blog'),
    path("restaurant/<int:res_id>/",RestaurantBlogs.as_view(),name="res_blogs")
]