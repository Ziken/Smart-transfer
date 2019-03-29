from rest_framework.permissions import BasePermission, Http404
from .models import Category, Item


class CategoryUserPermission(BasePermission):
    def has_permission(self, request, view):
        if request.method == "POST":
            id_parent = request.POST.get("id_parent", None)
            category = Category.objects.filter(id=id_parent)
            if category.exists():
                return category.first().created_by == request.user
            if id_parent:
                return False

        return True


    def has_object_permission(self, request, view, obj):
        if not obj:
            return False
        return obj.created_by == request.user


class ItemUserPermission(BasePermission):
    def has_permission(self, request, view):
        if request.method == "POST":
            id_category = request.POST.get("id_category", None)
            if id_category:
                category = Category.objects.filter(id=id_category)
                return category.exists() and category.first().created_by == request.user

            return False

        return True

    def has_object_permission(self, request, view, obj):
        if not obj:
            return False
        return request.user == obj.id_category.created_by
