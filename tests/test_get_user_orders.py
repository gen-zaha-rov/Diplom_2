import allure
import burgers_api
import data


class TestGetUsersOrders:
    @allure.title("Успешное получение списка заказов авторизованного пользователя")
    @allure.description("Проверка успешности получения cписка заказов авторизованного пользователя")
    def test_get_orders_auth_users_success(self, default_user, default_burger):
        with allure.step("Авторизоваться и подготовить заголовки"):
            user_response, access_token = default_user
            headers = {"Authorization": access_token}
        with allure.step("Подготовить ингредиенты бургера"):
            ingredients = default_burger
        with allure.step("Создать два заказа"):
            burgers_api.create_new_order(headers, ingredients)
            burgers_api.create_new_order(headers, ingredients)
        with allure.step("Получить список заказов пользователя"):
            user_orders = burgers_api.get_users_orders(headers)
        with allure.step("Проверить успешный статус и наличие заказов"):
            assert user_orders.status_code == 200
            assert user_orders.json()["orders"][0] != None
            assert user_orders.json()["orders"][1] != None

    @allure.title("Ошибка 401 при получении списка заказов неавторизованным пользователем")
    @allure.description("Проверка получения ошибки 401 Unauthorized при попытке получения cписка заказов неавторизованным пользователем")
    def test_get_order_list_not_auth_user_fail(self, default_burger):
        with allure.step("Подготовить ингредиенты бургера"):
            ingredients = default_burger
        with allure.step("Создать два заказа без авторизации"):
            burgers_api.create_new_order(None, ingredients)
            burgers_api.create_new_order(None, ingredients)
        with allure.step("Попытаться получить список заказов без авторизации"):
            orders_response = burgers_api.get_users_orders(None)
        with allure.step("Проверить статус 401 и корректное сообщение"):
            assert orders_response.status_code == 401
            assert orders_response.json()["message"] == data.NOT_AUTHORIZED_MSG