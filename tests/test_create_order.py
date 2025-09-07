import allure
import burgers_api
import data
import pytest


class TestCreateOrder:
    @allure.title("Успешное создание заказа с ингредиентами авторизованным пользователем")
    @allure.description("Проверка успешности авторизации и создания заказа")
    def test_create_order_burger_auth_user_success(self, default_burger, default_user):
        user_response, access_token = default_user
        headers = {"Authorization": access_token}
        create_response = burgers_api.create_new_order(headers, default_burger)
        assert create_response.status_code == 200 and create_response.json()["order"]["number"] != None

    @allure.title("Ошибка 400 Bad Request если оформить пустой заказ авторизованным пользователем")
    @allure.description("При пустом заказе авторизованным пользователем сервис возвращает ошибку 400 Bad Request")
    def test_create_order_without_burger_auth_user_fail(self, default_user):
        user_response, access_token = default_user
        headers = {"Authorization": access_token}
        create_response = burgers_api.create_new_order(headers, None)
        assert create_response.status_code == 400 and create_response.json()["message"] == data.EMPTY_ORDER_AUTH_MSG


    @allure.title("Ошибка 401 Unauthorized если сделать заказ неавторизованным пользователем")
    @allure.description("Неавторизованный пользователь не может сделать заказ, сервис возвращает ошибку 401 Unauthorized")
    def test_create_order_burger_not_auth_user_fail(self, default_burger):
        create_response = burgers_api.create_new_order(None, default_burger)
        assert create_response.status_code == 401  # Здесь ошибка в системе, потому что вместо ошибки 401 система разрешает неавторизованному пользователю делать заказ


    @allure.title("Ошибка 400 Bad Request если сделать пустой заказ неавторизованным пользователем")
    @allure.description("При пустом заказе неавторизованным пользователем сервис возвращает ошибку 400 Bad Request")
    def test_create_order_without_burger_not_auth_user_fail(self):
        create_response = burgers_api.create_new_order(None, None)
        assert create_response.status_code == 400 and create_response.json()["message"] == data.EMPTY_ORDER_NOT_AUTH_MSG

    @allure.title("Ошибка 500 Internal Server Error при заказе авторизованным пользователем с невалидным хешем ингредиента")
    @allure.description("Если сделать заказ авторизованным пользователем и указать ингредиенты с невалидным хешем, то сервис вернёт ошибку 500 Internal Server Error")
    def test_create_order_auth_user_wrong_hash_fail(self, default_user):
        user_response, access_token = default_user
        headers = {"Authorization": access_token}
        ingredients = data.WRONG_INGREDIENTS
        create_response = burgers_api.create_new_order(headers, ingredients)
        assert create_response.status_code == 500

    @allure.title("Ошибка 500 Internal Server Error если сделать заказ неавторизованным пользователем с невалидным хешем ингредиента")
    @allure.description("Если сделать заказ неавторизованным пользователем и указать ингредиенты с невалидным хешем, то сервис вернёт ошибку 500 Internal Server Error")
    def test_create_order_not_auth_user_wrong_hash_fail(self):
        ingredients = data.WRONG_INGREDIENTS
        create_response = burgers_api.create_new_order(None, ingredients)
        assert create_response.status_code == 500