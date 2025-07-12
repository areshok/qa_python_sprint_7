import requests
import allure


class BaseRequest:

    @allure.step("Отправка get запроса")
    def get(self, *args, **kwargs):
        return requests.get(*args, **kwargs)

    @allure.step("Отправка post запроса")
    def post(self, *args, **kwargs):
        return requests.post(*args, **kwargs)

    @allure.step("Получение json текста ответа")
    def response_json(self, response):
        return response.json()

    @allure.step("Получение статуса ответа")
    def status(self, response):
        return response.status_code
