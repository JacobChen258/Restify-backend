from rest_framework.generics import ListAPIView
from restaurants.serializers import RestaurantSearchSerializer
from rest_framework.permissions import IsAuthenticated
from restaurants.models import Restaurant
from menu_items.models import MenuItem
from pagination import SearchResultsSetPagination
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST

class RestaurantSearch(ListAPIView):
    serializer_class = RestaurantSearchSerializer
    pagination_class = SearchResultsSetPagination
    
    def get(self, request, *args, **kwargs):
        if self.kwargs['method'] not in ["name","address","item"]:
            return Response(status=HTTP_400_BAD_REQUEST)
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        if 'field' in self.kwargs:
            if self.kwargs['method'] == "name":
                return Restaurant.objects.filter(name__icontains = self.kwargs['field']).order_by('-num_followers')
            elif self.kwargs['method'] == 'address':
                return Restaurant.objects.filter(address__icontains = self.kwargs['field']).order_by('-num_followers')
            else:
                items =  MenuItem.objects.filter(name__icontains=self.kwargs['field'])
                res = list(set([item.restaurant for item in items]))
                return sorted(res, key=lambda item: item.num_followers)
        else:
            return Restaurant.objects.all().order_by('-num_followers')
