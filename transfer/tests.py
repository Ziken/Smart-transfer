from django.contrib.auth import get_user_model
from django.shortcuts import reverse

from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from rest_framework.authtoken.models import Token
from .models import Category, Item


class TestCategory(APITestCase):
    def setUp(self):
        User = get_user_model()
        self.username = "test"
        self.email = "test@test.test"
        self.password="test123"
        self.user_1 = User.objects.create_user(username=self.username, email=self.email, password=self.password)
        self.user_2 = User.objects.create_user(username=self.username+"_1", email=self.email, password=self.password)

        self.client = APIClient()
        is_logged = self.client.login(username=self.username, password=self.password)
        self.assertEqual(is_logged, True)

        self.categories = [
            Category.objects.create(name="test_1", created_by=self.user_1),
            Category.objects.create(name="test_2", created_by=self.user_2)
        ]


    def test_category_if_user_is_not_logged(self):
        self.client.logout()
        entry = self.categories[0]
        url = reverse("category_details", kwargs={"pk": entry.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_category(self):
        entry = self.categories[0]
        url = reverse("category_details", kwargs={"pk": entry.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get("id"), entry.id)
        self.assertEqual(response.data.get("name"), entry.name)
        self.assertEqual(response.data.get("created_by"), entry.created_by_id)

    def test_get_non_existed_category(self):
        id_cat = 999
        url = reverse("category_details", kwargs={"pk": id_cat})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_category_of_other_user(self):
        entry = self.categories[1]
        url = reverse("category_details", kwargs={"pk": entry.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_insert_category(self):
        new_name = "some_new_unique_name"
        user = self.user_1
        url = reverse("category_insert")
        response = self.client.post(url, data={
            "name": new_name,
            "created_by": user.id
        })

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Category.objects.filter(name=new_name))

    def test_insert_category_if_user_is_not_logged(self):
        self.client.logout()
        new_name = "some_new_unique_name"
        user = self.user_1
        url = reverse("category_insert")
        response = self.client.post(url, data={
            "name": new_name,
            "created_by": user.id
        })

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertFalse(Category.objects.filter(name=new_name))

    def test_modify_category(self):
        entry = self.categories[0]
        new_name = "new_test_name"
        url = reverse("category_details", kwargs={"pk": entry.id})
        response = self.client.patch(url, data={"name": new_name})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get("name"), new_name)
        self.assertTrue(Category.objects.filter(id=entry.id, name=new_name).exists())

    def test_modify_non_existed_category(self):
        id_cat = 999
        url = reverse("category_details", kwargs={"pk": id_cat})
        response = self.client.patch(url, data={"name": "new_name"})
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_modify_category_of_other_user(self):
        entry = self.categories[1]
        url = reverse("category_details", kwargs={"pk": entry.id})
        response = self.client.patch(url, data={"name": "new_name"})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_remove_category(self):
        entry = self.categories[0]
        url = reverse("category_details", kwargs={"pk": entry.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Category.objects.filter(id=entry.id))

    def test_remove_category_of_other_user(self):
        entry = self.categories[1]
        url = reverse("category_details", kwargs={"pk": entry.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertTrue(Category.objects.filter(id=entry.id))



class TestItem(APITestCase):
    def setUp(self):
        User = get_user_model()
        self.username = "test"
        self.email = "test@test.test"
        self.password = "test123"
        self.user_1 = User.objects.create_user(username=self.username, email=self.email, password=self.password)
        self.user_2 = User.objects.create_user(username=self.username + "_1", email=self.email, password=self.password)

        self.client = APIClient()
        is_logged = self.client.login(username=self.username, password=self.password)
        self.assertEqual(is_logged, True)

        self.categories = [
            Category.objects.create(name="test_1", created_by=self.user_1),
            Category.objects.create(name="test_2", created_by=self.user_2)
        ]
        self.items = [
            Item.objects.create(name="item_1", id_category=self.categories[0]),
            Item.objects.create(name="item_2", id_category=self.categories[0]),
            Item.objects.create(name="item_3", id_category=self.categories[1]),
            Item.objects.create(name="item_4", id_category=self.categories[1]),
        ]

    def test_get_item(self):
        entry = self.items[0]
        url = reverse("item_details", kwargs={"pk": entry.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get("id"), entry.id)
        self.assertEqual(response.data.get("name"), entry.name)

    def test_get_non_existed_item(self):
        id_entry = 999
        url = reverse("item_details", kwargs={"pk": id_entry})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_item_of_other_user(self):
        entry = self.items[2]
        url = reverse("item_details", kwargs={"pk": entry.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_item_if_user_is_not_logged(self):
        self.client.logout()
        entry = self.items[0]
        url = reverse("item_details", kwargs={"pk": entry.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_insert_item(self):
        name = "some_test_unique_item_name"
        category = self.categories[0]
        url = reverse("item_insert")

        response = self.client.post(url, data={
            "name": name,
            "id_category": category.id
        })

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Item.objects.filter(name=name).exists())

    def test_insert_item_to_category_of_other_user(self):
        name = "some_test_unique_item_name"
        category = self.categories[1]
        url = reverse("item_insert")

        response = self.client.post(url, data={
            "name": name,
            "id_category": category.id
        })

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertFalse(Item.objects.filter(name=name).exists())

    def test_insert_item_to_non_existed_category(self):
        name = "some_test_unique_item_name"
        category_id = 999
        url = reverse("item_insert")

        response = self.client.post(url, data={
            "name": name,
            "id_category": category_id
        })
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertFalse(Item.objects.filter(name=name).exists())

    def test_modify_item(self):
        new_name = "Some new test name"
        item = self.items[0]

        url = reverse("item_details", kwargs={"pk": item.id})
        response = self.client.patch(url, data={"name": new_name})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(Item.objects.filter(name=new_name).exists())

    def test_modify_item_of_other_user(self):
        new_name = "Some new test name"
        item = self.items[-1]

        url = reverse("item_details", kwargs={"pk": item.id})
        response = self.client.patch(url, data={"name": new_name})

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertFalse(Item.objects.filter(name=new_name).exists())

    def test_modify_item_of_non_existed_item(self):
        new_name = "Some new test name"
        item_id = 999

        url = reverse("item_details", kwargs={"pk": item_id})
        response = self.client.patch(url, data={"name": new_name})

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertFalse(Item.objects.filter(name=new_name).exists())

    def test_remove_item(self):
        item = self.items[0]

        url = reverse("item_details", kwargs={"pk": item.id})
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Item.objects.filter(id=item.id).exists())

    def test_remove_item_of_other_user(self):
        item = self.items[-1]

        url = reverse("item_details", kwargs={"pk": item.id})
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertTrue(Item.objects.filter(id=item.id).exists())

    def test_remove_item_when_user_is_not_logged(self):
        self.client.logout()
        item = self.items[0]

        url = reverse("item_details", kwargs={"pk": item.id})
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertTrue(Item.objects.filter(id=item.id).exists())


class TestItemCategory(APITestCase):
    def setUp(self):
        User = get_user_model()
        self.username = "test"
        self.email = "test@test.test"
        self.password = "test123"
        self.user_1 = User.objects.create_user(username=self.username, email=self.email, password=self.password)
        self.user_2 = User.objects.create_user(username=self.username + "_1", email=self.email, password=self.password)

        self.client = APIClient()
        is_logged = self.client.login(username=self.username, password=self.password)
        self.assertEqual(is_logged, True)

        self.categories = [
            Category.objects.create(name="test_1", created_by=self.user_1),
            Category.objects.create(name="test_2", created_by=self.user_2)
        ]
        self.categories.append(Category.objects.create(name="sub_test_1", created_by=self.user_1, id_parent=self.categories[0]))

        self.items = [
            Item.objects.create(name="item_1", id_category=self.categories[0]),
            Item.objects.create(name="item_2", id_category=self.categories[0]),
            Item.objects.create(name="item_3", id_category=self.categories[1]),
            Item.objects.create(name="item_4", id_category=self.categories[1]),
        ]

    def test_get_category_item(self):
        url = reverse("category_item_list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get("categories")[0]["id"], self.categories[0].id)

    def test_subcategory_item(self):
        url = reverse("category_item_list", kwargs={"id_parent": self.categories[0].id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data.get("items"))

    def test_get_category_item_of_other_user(self):
        url = reverse("category_item_list", kwargs={"id_parent": self.categories[1].id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertFalse(response.data.get("categories"))
        self.assertFalse(response.data.get("items"))

    def test_get_non_existing_category(self):
        id_cat = 999
        url = reverse("category_item_list", kwargs={"id_parent": id_cat})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_category_item_when_user_is_not_logged(self):
        self.client.logout()
        url = reverse("category_item_list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class TestUser(APITestCase):
    def setUp(self):
        self.User = get_user_model()
        self.username = "test"
        self.email = "test@test.test"
        self.password = "test123"
        self.client = APIClient()

    def create_user(self):
        url = reverse("user_create")
        response = self.client.post(url, data={
            "username": self.username,
            "password": self.password,
            "email": self.email
        })

        return response

    def test_create_user(self):
        response = self.create_user()

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data.get("username"), self.username)
        self.assertTrue(self.User.objects.filter(username=self.username).exists())
        self.assertTrue(Token.objects.all().exists())

    def test_user_login(self):
        self.create_user()

        url = reverse("user_login")
        response = self.client.post(url, data={
            "username": self.username,
            "password": self.password
        })

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(Token.objects.filter(key=response.data.get("token")).exists())

    def test_user_with_wrong_credentials(self):
        url = reverse("user_login")
        response = self.client.post(url, data={
            "username": "some_user",
            "password": "some_password"
        })

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
