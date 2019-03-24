from django.urls import path
from .views import CategoryItemListView, ItemView, ItemInsertView, CategoryView, CategoryInsertView, UserCreate, LoginView

urlpatterns = [
    path("category-item/", CategoryItemListView.as_view(), name="category_item_list"),
    path("category-item/<int:id_parent>", CategoryItemListView.as_view(), name="category_item_list"),
    path("item/<int:pk>", ItemView.as_view(), name="item_details"),
    path("item/", ItemInsertView.as_view(), name="item_insert"),
    path("category/<int:pk>", CategoryView.as_view(), name="category_details"),
    path("category/", CategoryInsertView.as_view(), name="category_insert"),

    path('user/', UserCreate.as_view(), name="user_create"),
    path("login/", LoginView.as_view(), name="user_login"),
]
