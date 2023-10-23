from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase

User = get_user_model()


class UserTests(APITestCase):

    def test_create_account(self):
        """
        Ensure we can create a new account object.
        """
        url = 'http://localhost/api/users/'
        data = {
            "email": "vpupkin@yandex.ru",
            "username": "vasya.pupkin",
            "first_name": "Вася",
            "last_name": "Пупкин",
            "password": "1Qwerty123"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get().username, 'vasya.pupkin')
        self.assertEqual(User.objects.get().email, 'vpupkin@yandex.ru')
        self.assertEqual(User.objects.get().first_name, "Вася",)
        self.assertEqual(User.objects.get().last_name, "Пупкин",)
