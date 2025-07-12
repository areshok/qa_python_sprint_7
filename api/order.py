import json
import allure

from .base import BaseRequest

from ..urls import URLS


class OrderRequest(BaseRequest):

    @allure.step("Создание заказа")
    def create(self, data):
        headers = {
            "Content-Type": "application/json"
        }
        response = self.post(
            url=URLS["api"]["order"]["create"],
            data=json.dumps(data),
            headers=headers
        )
        status = self.status(response)
        body = self.response_json(response)
        return {"response": body, "status": status}

    @allure.step("Получение списка заказов")
    def list(self):
        response = self.get(url=URLS["api"]["order"]["list"])
        status = self.status(response)
        body = self.response_json(response)
        return {"response": body, "status": status}
