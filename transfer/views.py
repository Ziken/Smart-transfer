from django.core import exceptions
from django.contrib.auth import authenticate

from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from .models import Category, Item
from .serializers import ItemSerializer, CategorySerializer, UserSerializer, CategoryItemSerializer
from .permissions import CategoryUserPermission, ItemUserPermission


class CategoryItemListView(APIView):
    serializer_class = CategoryItemSerializer
    permission_classes = (IsAuthenticated, )

    def get(self, request, id_parent=None, **kwargs):
        id_user = request.user.id
        parent_category = Category.objects.filter(id=id_parent)
        if id_parent:
            if not parent_category:
                return Response({}, status=status.HTTP_404_NOT_FOUND)

            if not parent_category.filter(created_by=id_user):
                raise exceptions.PermissionDenied()

        categories = Category.objects.filter(id_parent=id_parent, created_by=id_user)
        items = Item.objects.filter(id_category=id_parent)
        serializer = self.serializer_class(categories=categories, items=items)
        return Response(serializer.data)


class ItemView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated, ItemUserPermission,)
    queryset = Item.objects.all()
    serializer_class = ItemSerializer


class ItemInsertView(generics.CreateAPIView):
    permission_classes = (IsAuthenticated, ItemUserPermission,)
    serializer_class = ItemSerializer


class CategoryView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated, CategoryUserPermission,)
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class CategoryInsertView(generics.CreateAPIView):
    permission_classes = (IsAuthenticated, CategoryUserPermission,)
    serializer_class = CategorySerializer


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
