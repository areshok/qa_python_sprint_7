import pytest
import allure

from ..api.order import OrderRequest
from ..data.function import generate_order
from ..data.models import Order, Station, Color


@pytest.mark.usefixtures("create_or_update_bd")
class TestCaseOrder:

    @pytest.mark.parametrize(
            "color", [1, 2, 3, 4]
    )
    @allure.title("""
    тест: тело ответа содержит track
    тест: можно указать один из цветов — BLACK или GREY
    тест: можно указать оба цвета
    тест: можно совсем не указывать цвет
    """)
    def test_create_order(self, color, database,):
        """
        тест: тело ответа содержит track
        тест: можно указать один из цветов — BLACK или GREY
        тест: можно указать оба цвета
        тест: можно совсем не указывать цвет
        """
        data = generate_order()
        station = database.get_one(Station, f"Station.name=='{data['metroStation']}'")
        color = database.get_one(Color, f"Color.id=='{color}'")
        data["color"] = color.name.split(",")
        new_data = data.copy()
        new_data['color'] = color.id
        new_data["metroStation"] = station.id
        order = Order(**new_data)
        database.write_one(order)
        response = OrderRequest().create(data)
        assert response['status'] == 201
        assert "track" in response["response"]

    @allure.title("тест: проверка тела списка заказов")
    def test_list_order_body_content(self):
        "тест: проверка тела списка заказов"
        response = OrderRequest().list()
        # проверка наличия ключей в теле ответа
        assert list(response["response"]) == ['orders', 'pageInfo', 'availableStations']
        # проверка наличия ключей в заказе
        assert "id" in response['response']["orders"][0]
        assert "courierId" in response['response']["orders"][0]
        assert "firstName" in response['response']["orders"][0]
        assert "lastName" in response['response']["orders"][0]
        assert "address" in response['response']["orders"][0]
        assert "metroStation" in response['response']["orders"][0]
        assert "phone" in response['response']["orders"][0]
        assert "rentTime" in response['response']["orders"][0]
        assert "deliveryDate" in response['response']["orders"][0]
        assert "track" in response['response']["orders"][0]
        assert "comment" in response['response']["orders"][0]
        assert "createdAt" in response['response']["orders"][0]
        assert "updatedAt" in response['response']["orders"][0]
        assert "updatedAt" in response['response']["orders"][0]
        assert "status" in response['response']["orders"][0]
        # првоерка наличия ключей в pageInfo
        assert "page" in response['response']["pageInfo"]
        assert "total" in response['response']["pageInfo"]
        assert "limit" in response['response']["pageInfo"]
        # првоерка наличия ключей в availableStations
        assert "name" in response['response']["availableStations"][0]
        assert "number" in response['response']["availableStations"][0]
        assert "color" in response['response']["availableStations"][0]
