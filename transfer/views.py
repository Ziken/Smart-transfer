from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.response import Response
from django.contrib.auth import authenticate
from django.shortcuts import get_object_or_404
from rest_framework import status
from django.core import exceptions

from .models import Category, Item
from .serializers import ItemSerializer, CategorySerializer, UserSerializer
from .permissions import CategoryUserPermission, ItemUserPermission
from rest_framework.permissions import IsAuthenticated


class CategoryItemListView(APIView):

    def get(self, request, id_parent=None):
        id_user = request.user.id
        parent_category = Category.objects.filter(id=id_parent)
        if id_parent:
            if not parent_category:
                return Response({}, status=status.HTTP_404_NOT_FOUND)

            if not parent_category.filter(created_by=id_user):
                raise exceptions.PermissionDenied()

        categories = Category.objects.filter(id_parent=id_parent, created_by=id_user)
        items = Item.objects.filter(id_category=id_parent)
        data = {
            "categories": list(categories.values("id", "name", "created_date")),
            "items": list(items.values("id", "name", "description", "created_date"))
        }
        return Response(data)


class ItemView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (ItemUserPermission, )
    queryset = Item.objects.all()
    serializer_class = ItemSerializer


class ItemInsertView(generics.CreateAPIView):
    serializer_class = ItemSerializer
    permission_classes = (ItemUserPermission, )

class CategoryView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated, CategoryUserPermission,)
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class CategoryInsertView(generics.CreateAPIView):
    serializer_class = CategorySerializer
    permission_classes = (IsAuthenticated, CategoryUserPermission,)

    def post(self, request, *args, **kwargs):
        p = request.POST
        new_category = CategorySerializer(data={
            "id_parent": p.get("id_parent"),
            "name": p.get("name"),
            "created_by": request.user.id
        })
        if new_category.is_valid(True):
            new_category.save()
            return Response(new_category.data, status=status.HTTP_201_CREATED)


class UserCreate(generics.CreateAPIView):
    authentication_classes = ()
    permission_classes = ()
    serializer_class = UserSerializer


class LoginView(APIView):
    permission_classes = ()

    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        user = authenticate(username=username, password=password)
        if user:
            return Response({"token": user.auth_token.key})

        return Response({"error": "Wrong Credentials"}, status=status.HTTP_400_BAD_REQUEST)
