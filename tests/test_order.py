import pytest
import allure

from .base import BaseTestCase

from ..api.order import OrderRequest
from ..data.models import Order


class TestCaseOrder(BaseTestCase):

    @pytest.mark.parametrize(
            "color", ["BLACK", "GREY", ["BLACK", "GREY"], None]
    )
    @allure.title("""
    тест: тело ответа содержит track
    тест: можно указать один из цветов — BLACK или GREY
    тест: можно указать оба цвета
    тест: можно совсем не указывать цвет
    """)
    def test_create_order(self, color):
        """
        тест: тело ответа содержит track
        тест: можно указать один из цветов — BLACK или GREY
        тест: можно указать оба цвета
        тест: можно совсем не указывать цвет
        """
        data = Order().get()
        if color is None:
            data.pop("color")
        else:
            data["color"] = [color]
        response = OrderRequest().create(data)
        self.assertEqual(response['status'], 201)
        self.assertIn("track", response["response"])

    @allure.title("тест: проверка тела списка заказов")
    def test_list_order_body_content(self):
        "тест: проверка тела списка заказов"
        response = OrderRequest().list()
        # проверка наличия ключей в теле ответа
        self.assertEqual(
            list(response["response"]),
            ['orders', 'pageInfo', 'availableStations']
        )
        # проверка наличия ключей в заказе
        self.assertIn("id", response['response']["orders"][0])
        self.assertIn("courierId", response['response']["orders"][0])
        self.assertIn("firstName", response['response']["orders"][0])
        self.assertIn("lastName", response['response']["orders"][0])
        self.assertIn("address", response['response']["orders"][0])
        self.assertIn("metroStation", response['response']["orders"][0])
        self.assertIn("phone", response['response']["orders"][0])
        self.assertIn("rentTime", response['response']["orders"][0])
        self.assertIn("deliveryDate", response['response']["orders"][0])
        self.assertIn("track", response['response']["orders"][0])
        self.assertIn("comment", response['response']["orders"][0])
        self.assertIn("createdAt", response['response']["orders"][0])
        self.assertIn("updatedAt", response['response']["orders"][0])
        self.assertIn("status", response['response']["orders"][0])
        # првоерка наличия ключей в pageInfo
        self.assertIn("page", response['response']["pageInfo"])
        self.assertIn("total", response['response']["pageInfo"])
        self.assertIn("limit", response['response']["pageInfo"])
        # првоерка наличия ключей в availableStations
        self.assertIn("name", response['response']["availableStations"][0])
        self.assertIn("number", response['response']["availableStations"][0])
        self.assertIn("color", response['response']["availableStations"][0])
