from django.urls import path
from .views import MenuItemView

app_name = "menu_items"

urlpatterns = [
    path("add/",MenuItemView.as_view(),name='add_item'),
    path("<int:item_id>/",MenuItemView.as_view(),name="menu_item"),
    path("restaurant/<int:res_id>/",MenuItemView.as_view(),name="restaurant_items")
]