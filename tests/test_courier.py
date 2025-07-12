import allure
import pytest

from ..api.courier import CourierRequest
from ..settings import CREATED_COURIER
from ..data.models import User as User
from ..data.function import generate_user


@pytest.mark.usefixtures("create_or_update_bd")
class TestCaseCourier:

    @allure.title("""
    тест: проверка регистрации курьера, проверка успешнего ответа
    тест: успешный запрос возвращает {{"ok":true}}
    """)
    def test_create_courier(self, database):
        """
        тест: проверка регистрации курьера, проверка успешнего ответа
        тест: успешный запрос возвращает {"ok":true}
        """
        data = generate_user()
        courier = CourierRequest()
        user = User(**data)
        response = courier.registrate_courier(**data)
        assert response["status"] == 201
        assert response["response"][courier.ResponseField.create] is True
        database.write_one(user)

    @allure.title("""
    тест: првоерка что нельзя создать двух одинаковых курьеров
    тест: проверка появления ошибки при регистрации курьера
    с логиным который уже есть в системе
    """)
    def test_cant_create_two_identical_couriers(self, database):
        """
        тест: првоерка что нельзя создать двух одинаковых курьеров
        тест: проверка появления ошибки при регистрации курьера
        с логиным который уже есть в системе
        """
        data = generate_user()
        user = User(**data)
        courier = CourierRequest()
        response = courier.registrate_courier(**data)
        assert response["status"] == 201
        assert response["response"][courier.ResponseField.create] is True
        database.write_one(user)
        response = courier.registrate_courier(**data)
        assert response["status"] == 409
        assert courier.ResponseText.dublicat_user in response["response"][courier.ResponseField.err]

    @allure.title(
        "тест: регистрация курьера заполнены обязательные поля (логин, пароль)"
        )
    def test_registercourier_fields_login_password(self, database):
        "тест: регистрация курьера заполнены обязательные поля (логин, пароль)"
        data = generate_user()
        user = User(**data)
        courier = CourierRequest()
        response = courier.registrate_courier(
            login=user.login, password=user.password
        )
        assert response["status"] == 201
        assert response["response"][courier.ResponseField.create] is True
        database.write_one(user)

    @allure.title("""
    тест: проверка появление ошибки при регистрации пользователя,
    поле login отсутсвует
    """)
    def test_error_occurrence_is_missing_field_login(self):
        """
        тест: проверка появление ошибки при регистрации пользователя,
        поле login отсутсвует
        """
        data = generate_user()
        user = User(**data)
        courier = CourierRequest()
        response = courier.registrate_courier(
            password=user.password, firstname=user.firstname)
        assert response["status"] == 400
        assert courier.ResponseText.missing_field_register in response["response"][courier.ResponseField.err]

    @allure.title("""
    тест: проверка появление ошибки при регистрации пользователя,
    поле password отсутсвует
    """)
    def test_error_occurrence_is_missing_field_password(self):
        """
        тест: проверка появление ошибки при регистрации пользователя,
        поле password отсутсвует
        """
        user = User(**generate_user())
        courier = CourierRequest()
        response = courier.registrate_courier(
            password=user.login, firstname=user.firstname)
        assert response["status"] == 400
        assert courier.ResponseText.missing_field_register in response["response"][courier.ResponseField.err]

    @allure.title("""
    тест: проверка появление ошибки при регистрации пользователя,
    поле firstaname отсутсвует
    """)
    def test_error_occurrence_is_missing_field_firstname(self):
        """
        тест: проверка появление ошибки при регистрации пользователя,
        поле firstaname отсутсвует
        """
        user = User(**generate_user())
        courier = CourierRequest()
        response = courier.registrate_courier(
            password=user.login, firstname=user.password)
        assert response["status"] == 400
        assert courier.ResponseText.missing_field_register in response["response"][courier.ResponseField.err]

    @allure.title("""
    тест: проверка авторизации курьера
    тест: для авторизации нужно передать все обязательные поля
    """)
    def test_courier_log_in(self):
        """
        тест: проверка авторизации курьера
        тест: для авторизации нужно передать все обязательные поля
        """
        courier = CourierRequest()
        response = courier.login_courier(**CREATED_COURIER)
        assert response["status"] == 200
        assert courier.ResponseField.login in response["response"]

    @allure.title("""
    тест: проверка появление ошибки при отсутсвии поля логина
    """)
    def test_courier_log_in_missing_loggin(self):
        "тест: проверка появление ошибки при отсутсвии поля логина"
        courier = CourierRequest()
        data = {"password": CREATED_COURIER["password"]}
        response = courier.login_courier(**data)
        assert response["status"] == 400
        assert response["response"][courier.ResponseField.err] == courier.ResponseText.missing_field_login

    @allure.title("""
    тест: проверка появление ошибки при отсутсвии поля пароля
    """)
    def test_courier_log_in_missing_password(self):
        "тест: проверка появление ошибки при отсутсвии поля пароля"
        courier = CourierRequest()
        data = {"password": CREATED_COURIER["login"]}
        response = courier.login_courier(**data)
        assert response["status"] == 400
        assert response["response"][courier.ResponseField.err] == courier.ResponseText.missing_field_login

    @allure.title("""
    тест: появление ошибки при попытке входа в систему с несуществующем логоном
    """)
    def test_an_error_occurs_with_a_non_existent_login(self):
        """
        тест: появление ошибки при попытке входа в систему
        с несуществующем логином.
        """
        courier = CourierRequest()
        user = User(**generate_user())
        response = courier.login_courier(
            **{"login": user.login, "password": user.password})
        assert response["status"] == 404
        assert response["response"][courier.ResponseField.err] == courier.ResponseText.non_existent
