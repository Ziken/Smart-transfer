from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.response import Response
from django.contrib.auth import authenticate
from django.shortcuts import get_object_or_404
from rest_framework import status
from django.core import exceptions
from .models import Category, Item
from .serializers import ItemSerializer, CategorySerializer, UserSerializer


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
    queryset = Item.objects.all()
    serializer_class = ItemSerializer

    def get_object(self):
        obj = get_object_or_404(self.get_queryset(), pk=self.kwargs["pk"])
        parent = obj.id_category
        if parent.created_by != self.request.user:
            raise exceptions.PermissionDenied()

        self.check_object_permissions(self.request, obj)

        return obj


class ItemInsertView(generics.CreateAPIView):
    serializer_class = ItemSerializer

    def post(self, request, *args, **kwargs):
        id_parent = request.POST.get("id_category")
        parent_category = Category.objects.filter(id=id_parent, created_by=self.request.user.id)
        if not parent_category:
            raise exceptions.PermissionDenied()

        return super().create(request, *args, **kwargs)


class CategoryView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def get_object(self):
        obj = get_object_or_404(self.get_queryset(), pk=self.kwargs["pk"])
        self.check_object_permissions(self.request, obj)
        if obj.created_by.id != self.request.user.id:
            raise exceptions.PermissionDenied()

        return obj


class CategoryInsertView(generics.CreateAPIView):
    serializer_class = CategorySerializer

    def post(self, request, *args, **kwargs):
        id_parent = request.POST.get("id_parent")
        if id_parent and not Category.objects.filter(id=id_parent, created_by=request.user.id).exists():
            raise exceptions.PermissionDenied()

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
