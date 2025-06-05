import allure

from .base import BaseTestCase

from ..api.courier import CourierRequest
from ..data.models import User
from ..settings import CREATED_COURIER


class TestCaseCourier(BaseTestCase):

    @allure.title("""
    тест: проверка регистрации курьера, проверка успешнего ответа
    тест: успешный запрос возвращает {{"ok":true}}
    """)
    def test_create_courier(self):
        """
        тест: проверка регистрации курьера, проверка успешнего ответа
        тест: успешный запрос возвращает {"ok":true}
        """
        user = User()
        courier = CourierRequest()
        response = courier.registrate_courier(**user.get())
        self.assertEqual(response["status"], 201)
        self.assertTrue(response["response"][courier.ResponseField.create])
        user.save()

    @allure.title("""
    тест: првоерка что нельзя создать двух одинаковых курьеров
    тест: проверка появления ошибки при регистрации курьера
    с логиным который уже есть в системе
    """)
    def test_cant_create_two_identical_couriers(self):
        """
        тест: првоерка что нельзя создать двух одинаковых курьеров
        тест: проверка появления ошибки при регистрации курьера
        с логиным который уже есть в системе
        """
        user = User()
        courier = CourierRequest()
        response = courier.registrate_courier(**user.get())
        self.assertEqual(response["status"], 201)
        self.assertTrue(response["response"][courier.ResponseField.create])
        user.save()
        response = courier.registrate_courier(**user.get())
        self.assertEqual(response["status"], 409)
        self.assertIn(
            courier.ResponseText.dublicat_user,
            response["response"][courier.ResponseField.err]
        )

    @allure.title(
        "тест: регистрация курьера заполнены обязательные поля (логин, пароль)"
        )
    def test_registercourier_fields_login_password(self):
        "тест: регистрация курьера заполнены обязательные поля (логин, пароль)"
        user = User()
        courier = CourierRequest()
        response = courier.registrate_courier(
            login=user.login, password=user.password
        )
        self.assertEqual(response["status"], 201)
        self.assertTrue(response["response"][courier.ResponseField.create])
        user.save()

    @allure.title("""
    тест: проверка появление ошибки при регистрации пользователя,
    поле login отсутсвует
    """)
    def test_error_occurrence_is_missing_field_login(self):
        """
        тест: проверка появление ошибки при регистрации пользователя,
        поле login отсутсвует
        """
        user = User()
        courier = CourierRequest()
        response = courier.registrate_courier(
            password=user.password, firstname=user.firstname)
        self.assertEqual(response["status"], 400)
        self.assertIn(
            courier.ResponseText.missing_field_register,
            response["response"][courier.ResponseField.err]
        )

    @allure.title("""
    тест: проверка появление ошибки при регистрации пользователя,
    поле password отсутсвует
    """)
    def test_error_occurrence_is_missing_field_password(self):
        """
        тест: проверка появление ошибки при регистрации пользователя,
        поле password отсутсвует
        """
        user = User()
        courier = CourierRequest()
        response = courier.registrate_courier(
            password=user.login, firstname=user.firstname)
        self.assertEqual(response["status"], 400)
        self.assertIn(
            courier.ResponseText.missing_field_register,
            response["response"][courier.ResponseField.err]
        )

    @allure.title("""
    тест: проверка появление ошибки при регистрации пользователя,
    поле firstaname отсутсвует
    """)
    def test_error_occurrence_is_missing_field_firstname(self):
        """
        тест: проверка появление ошибки при регистрации пользователя,
        поле firstaname отсутсвует
        """
        user = User()
        courier = CourierRequest()
        response = courier.registrate_courier(
            password=user.login, firstname=user.password)
        self.assertEqual(response["status"], 400)
        self.assertIn(
            courier.ResponseText.missing_field_register,
            response["response"][courier.ResponseField.err]
        )

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
        self.assertEqual(response["status"], 200)
        self.assertIn(courier.ResponseField.login, response["response"])

    @allure.title("""
    тест: проверка появление ошибки при отсутсвии поля логина
    """)
    def test_courier_log_in_missing_loggin(self):
        "тест: проверка появление ошибки при отсутсвии поля логина"
        courier = CourierRequest()
        data = {"password": CREATED_COURIER["password"]}
        response = courier.login_courier(**data)
        self.assertEqual(response["status"], 400)
        self.assertEqual(
            response["response"][courier.ResponseField.err],
            courier.ResponseText.missing_field_login
        )

    @allure.title("""
    тест: проверка появление ошибки при отсутсвии поля пароля
    """)
    def test_courier_log_in_missing_password(self):
        "тест: проверка появление ошибки при отсутсвии поля пароля"
        courier = CourierRequest()
        data = {"password": CREATED_COURIER["login"]}
        response = courier.login_courier(**data)
        self.assertEqual(response["status"], 400)
        self.assertEqual(
            response["response"][courier.ResponseField.err],
            courier.ResponseText.missing_field_login
        )

    @allure.title("""
    тест: появление ошибки при попытке входа в систему с несуществующем логоном
    """)
    def test_an_error_occurs_with_a_non_existent_login(self):
        """
        тест: появление ошибки при попытке входа в систему
        с несуществующем логином.
        """
        courier = CourierRequest()
        user = User()
        response = courier.login_courier(
            **{"login": user.login, "password": user.password})
        self.assertEqual(response["status"], 404)
        self.assertEqual(
            response["response"][courier.ResponseField.err],
            courier.ResponseText.non_existent
        )
