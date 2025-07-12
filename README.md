Сделаны тесты на регистрация и вход в систему курьера, получение списка заказов, создание заказа

Тесты курьера
- test_create_courier(self):
- test_cant_create_two_identical_couriers(self):
- test_registercourier_fields_login_password(self):
- test_error_occurrence_is_missing_field_login(self):
- test_error_occurrence_is_missing_field_password(self):
- test_error_occurrence_is_missing_field_firstname(self):
- test_courier_log_in(self):
- test_courier_log_in_missing_loggin(self):
- test_courier_log_in_missing_password(self):
- test_an_error_occurs_with_a_non_existent_login(self):

Тесты заказа:
 - test_create_order(self, color):
 - test_list_order_body_content(self):