from blogs.models import Blog
from blogs.models import Blog_Likes
from rest_framework.generics import RetrieveAPIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import get_object_or_404

class LikedBlog(RetrieveAPIView):
    permission_classes = [IsAuthenticated,]

    def get(self, request, *args, **kwargs):
        if 'blog_id' not in kwargs:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        like = Blog_Likes.objects.filter(blog=kwargs['blog_id'],user=request.user.id)
        return Response(status=status.HTTP_200_OK,data={"liked":len(like)>0})
