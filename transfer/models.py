from django.db import models


class Category(models.Model):
    id_parent = models.ForeignKey("Category", on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=150)
    created_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "categories"

    def __str__(self):
        return "{0} -> {1}: {2} ({3})".format(self.id_parent, self.id, self.name, self.created_date)


class Item(models.Model):
    name = models.CharField(max_length=200)
    status = models.CharField(max_length=100, blank=True)
    description = models.TextField(blank=True)
    created_date = models.DateTimeField(auto_now=True)

    id_category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
       return "{0} -> {1}: {2} ({3})".format(self.id_category, self.id, self.name, self.created_date)

