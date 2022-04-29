from blogs.models import Blog
from blogs.serializers.blog_like import LikedBlogSerializer
from blogs.models import Blog_Likes
from rest_framework.decorators import api_view,permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from restaurants.models import Restaurant
from notifications.serializers import NotificationsSerializer
from rest_framework.generics import get_object_or_404
@api_view(['POST','DELETE'])
@permission_classes((IsAuthenticated, ))
def liked_blog(request):
    print(request.method)
    if request.method=="POST":
        data = request.data.copy()
        if "blog" in request.data:
            blog = get_object_or_404(Blog,id=request.data['blog'])
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST,data={'detail':"missing blog id"})
        data['user'] = request.user.id
        if (len(Blog_Likes.objects.filter(blog=blog.id,user=request.user.id))>0):
            return Response(status = status.HTTP_409_CONFLICT,data={'detail':"you can't like a blog twice"})
        serializer = LikedBlogSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            blog.num_likes += 1
            blog.save()
            restaurant = blog.restaurant
            owner = restaurant.owner
            notif_data = {
                'viewer' : owner.id,
                'content': f"A user {request.user.first_name} {request.user.last_name} liked your blog {blog.title}"
            }
            notif_serializer = NotificationsSerializer(data=notif_data)
            notif_serializer.is_valid(raise_exception=True)
            notif_serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)   
    elif request.method == 'DELETE':
        if "id" not in request.data:
            return Response(status=status.HTTP_400_BAD_REQUEST,data={'detail':"missing blog id"})
        
        blog = get_object_or_404(Blog,id=request.data['id'])
        likes = Blog_Likes.objects.filter(blog=blog.id,user=request.user.id)
        if (len(Blog_Likes.objects.filter(blog=blog.id,user=request.user.id))==0):
            return Response(status = status.HTTP_404_NOT_FOUND,data={'detail':"you can't unlike a blog if you have not liked it"})
        for like in likes:
            like.delete()
            blog.num_likes -= 1
        blog.save()
        return Response(status=status.HTTP_204_NO_CONTENT)
    return Response(serializer.errors, status=status.HTTP_405_METHOD_NOT_ALLOWED)
