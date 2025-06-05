import allure


class BaseTestCase:
    @allure.step("Стравнение двух значений")
    def assertEqual(self, one, two):
        assert one == two

    @allure.step("Вхождение первого значения во второе")
    def assertIn(self, one, two):
        assert one in two

    @allure.step("Значение является правдой")
    def assertTrue(self, one):
        assert one is True
