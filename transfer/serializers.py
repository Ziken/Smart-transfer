from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.authtoken.models import Token

from .models import Category, Item


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("username", "email", "password")

        extra_kwargs = {
            "password": {"write_only": True}
        }

    def create(self, validated_data):
        user = User(
            email=validated_data["email"],
            username=validated_data["username"]
        )
        user.set_password(validated_data["password"])
        user.save()
        Token.objects.create(user=user)
        return user

class CategoryItemSerializer(serializers.Serializer):
    categories = serializers.SerializerMethodField()
    items = serializers.SerializerMethodField()

    def __init__(self, **kwargs):
        self.categories = kwargs.pop("categories")
        self.items = kwargs.pop("items")
        super().__init__(**kwargs)

    def get_categories(self):
        return CategorySerializer(
            self.categories,
            many=True
        ).data

    def get_items(self):
        return ItemSerializer(
            self.items,
            many=True
        ).data

    @property
    def data(self):
        return {
            "categories": self.get_categories(),
            "items": self.get_items()
        }