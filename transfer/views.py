from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.response import Response

from .models import Category, Item
from .serializers import ItemSerializer, CategorySerializer


class CategoryItemListView(APIView):
    def get(self, request, pk=None):
        categories = Category.objects.filter(id_parent=pk)
        items = Item.objects.filter(id_category=pk)
        print(categories.__dict__)
        data = {
            "categories": list(categories.values("id", "name", "created_date")),
            "items": list(items.values("id", "name", "description", "created_date"))
        }
        return Response(data)


class ItemView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer


class ItemInsertView(generics.CreateAPIView):
    serializer_class = ItemSerializer


class CategoryView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class CategoryInsertView(generics.CreateAPIView):
    serializer_class = CategorySerializer
