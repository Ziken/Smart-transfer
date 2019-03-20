from django.urls import path
from .views import CategoryItemListView, ItemView

urlpatterns = [
    # path("category/", category_list, name="category_list"),
    path("category-item/", CategoryItemListView.as_view(), name="category_item_list"),
    path("category-item/<int:pk>", CategoryItemListView.as_view(), name="category_item_list"),
    path("item/<int:pk>", ItemView.as_view(), name="item_details")
]
