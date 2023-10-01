from django.urls import reverse
from django.test import TestCase


class StatusCodeTest(TestCase):
    """
    Тесты на коды ответа.
    """

    def test_403_status(self):
        """
        Должен вернуть код 403,
        потому что метод GET не поддерживается для вью robot_create.
        """
        response = self.client.get(reverse("robot_create"))
        self.assertEqual(response.status_code, 403)

    def test_201_status(self):
        """
        Должен вернуть код 201,
        потому что данные в POST-запросе без ошибок.
        """
        response = self.client.post(reverse("robot_create"),
                                    {"model": "13", "version": "XS",
                                    "created": "2023-01-01 00:00:00"},
                                    content_type="application/json")
        self.assertEqual(response.status_code, 201)

    def test_400_status_validating_created(self):
        """
        Должен вернуть код 400,
        потому что в POST-запросе ошибка в поле created.
        """
        response = self.client.post(reverse("robot_create"),
                                    {"model": "13", "version": "XS",
                                    "created": "2023"},
                                    content_type="application/json")
        self.assertEqual(response.status_code, 400)

    def test_400_status_validating_model(self):
        """
        Должен вернуть код 400,
        потому что в POST-запросе ошибка в поле model.
        """
        response = self.client.post(reverse("robot_create"),
                                    {"model": "2big", "version": "XS",
                                    "created": "2023-01-01 00:00:00"},
                                    content_type="application/json")
        self.assertEqual(response.status_code, 400)

    def test_400_status_data_requirement(self):
        """
        Должен вернуть код 400,
        потому что в POST-запросе отсутствет поле version.
        """
        response = self.client.post(reverse("robot_create"),
                                    {"model": "13", "version": "2big",
                                    "created": "2023-01-01 00:00:00"},
                                    content_type="application/json")
        self.assertEqual(response.status_code, 400)
