import allure
import burgers_api
import data
import pytest


class TestCreateOrder:
    @allure.title("Успешное создание заказа с ингредиентами авторизованным пользователем")
    @allure.description("Проверка успешности авторизации и создания заказа")
    def test_create_order_burger_auth_user_success(self, default_burger, default_user):
        with allure.step("Авторизоваться и подготовить заголовки"):
            user_response, access_token = default_user
            headers = {"Authorization": access_token}
        with allure.step("Создать заказ с ингредиентами"):
            create_response = burgers_api.create_new_order(headers, default_burger)
        with allure.step("Проверить успешный статус и наличие номера заказа"):
            assert create_response.status_code == 200 and create_response.json()["order"]["number"] != None

    @allure.title("Ошибка 400 Bad Request если оформить пустой заказ авторизованным пользователем")
    @allure.description("При пустом заказе авторизованным пользователем сервис возвращает ошибку 400 Bad Request")
    def test_create_order_without_burger_auth_user_fail(self, default_user):
        with allure.step("Авторизоваться и подготовить заголовки"):
            user_response, access_token = default_user
            headers = {"Authorization": access_token}
        with allure.step("Попробовать создать пустой заказ"):
            create_response = burgers_api.create_new_order(headers, None)
        with allure.step("Проверить статус 400 и корректное сообщение"):
            assert create_response.status_code == 400 and create_response.json()["message"] == data.EMPTY_ORDER_AUTH_MSG


    @allure.title("Ошибка 401 Unauthorized если сделать заказ неавторизованным пользователем")
    @allure.description("Неавторизованный пользователь не может сделать заказ, сервис возвращает ошибку 401 Unauthorized")
    def test_create_order_burger_not_auth_user_fail(self, default_burger):
        with allure.step("Попробовать создать заказ без авторизации"):
            create_response = burgers_api.create_new_order(None, default_burger)
        with allure.step("Проверить статус 401"):
            assert create_response.status_code == 401  # Здесь ошибка в системе, потому что вместо ошибки 401 система разрешает неавторизованному пользователю делать заказ


    @allure.title("Ошибка 400 Bad Request если сделать пустой заказ неавторизованным пользователем")
    @allure.description("При пустом заказе неавторизованным пользователем сервис возвращает ошибку 400 Bad Request")
    def test_create_order_without_burger_not_auth_user_fail(self):
        with allure.step("Попробовать создать пустой заказ без авторизации"):
            create_response = burgers_api.create_new_order(None, None)
        with allure.step("Проверить статус 400 и корректное сообщение"):
            assert create_response.status_code == 400 and create_response.json()["message"] == data.EMPTY_ORDER_NOT_AUTH_MSG

    @allure.title("Ошибка 500 Internal Server Error при заказе авторизованным пользователем с невалидным хешем ингредиента")
    @allure.description("Если сделать заказ авторизованным пользователем и указать ингредиенты с невалидным хешем, то сервис вернёт ошибку 500 Internal Server Error")
    def test_create_order_auth_user_wrong_hash_fail(self, default_user):
        with allure.step("Авторизоваться и подготовить заголовки"):
            user_response, access_token = default_user
            headers = {"Authorization": access_token}
        with allure.step("Подготовить ингредиенты с невалидным хешем и оформить заказ"):
            ingredients = data.WRONG_INGREDIENTS
            create_response = burgers_api.create_new_order(headers, ingredients)
        with allure.step("Проверить статус 500"):
            assert create_response.status_code == 500

    @allure.title("Ошибка 500 Internal Server Error если сделать заказ неавторизованным пользователем с невалидным хешем ингредиента")
    @allure.description("Если сделать заказ неавторизованным пользователем и указать ингредиенты с невалидным хешем, то сервис вернёт ошибку 500 Internal Server Error")
    def test_create_order_not_auth_user_wrong_hash_fail(self):
        with allure.step("Подготовить ингредиенты с невалидным хешем"):
            ingredients = data.WRONG_INGREDIENTS
        with allure.step("Попробовать оформить заказ без авторизации"):
            create_response = burgers_api.create_new_order(None, ingredients)
        with allure.step("Проверить статус 500"):
            assert create_response.status_code == 500