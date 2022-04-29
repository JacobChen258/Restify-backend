from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from restaurants.models import Restaurant_Like
from rest_framework.generics import RetrieveAPIView


class LikedRestaurant(RetrieveAPIView):
    permission_classes = [IsAuthenticated,]

    def get(self, request, *args, **kwargs):
        if 'res_id' not in kwargs:
            return Response(status=status.HTTP_400_BAD_REQUEST,data={'detail':'missing restaurant id'})
        liked = len(Restaurant_Like.objects.filter(user=request.user.id,restaurant=kwargs['res_id']))
        return Response(status=status.HTTP_200_OK,data={"liked":liked>0})