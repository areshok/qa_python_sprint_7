import allure

from .base import BaseRequest
from ..urls import URLS


class CourierRequest(BaseRequest):
    class ResponseField:
        login = "id"
        err = "message"
        create = "ok"

    class ResponseText:
        dublicat_user = "Этот логин уже используется"
        missing_field_register = "Недостаточно данных для создания учетной записи"
        missing_field_login = "Недостаточно данных для входа"
        non_existent = "Учетная запись не найдена"

    @allure.step("Регистрация курьера")
    def registrate_courier(self, login=None, password=None, firstname=None):
        data = {}
        if login is not None:
            data["login"] = login
        if password is not None:
            data["password"] = password
        if firstname is not None:
            data["firstname"] = firstname
        response = self.post(url=URLS["api"]["courier"]["create"], data=data)
        status = self.status(response)
        body = self.response_json(response)
        return {"response": body, "status": status}

    @allure.step("Авторизиция курьера")
    def login_courier(self, login=None, password=None):
        data = {}
        if login is not None:
            data["login"] = login
        if password is not None:
            data["password"] = password
        response = self.post(url=URLS["api"]["courier"]["login"], data=data)
        status = self.status(response)
        body = self.response_json(response)
        return {"response": body, "status": status}
