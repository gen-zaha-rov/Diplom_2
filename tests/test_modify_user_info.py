import allure
import requests
import data
import urls
import burgers_api
import pytest


class TestChangeUserData:
    @allure.title("Проверка успешного изменения данных авторизованного пользователя")
    @allure.description("У авторизованного пользователя успешно редактируются данные для авторизации: email, name, password")
    @pytest.mark.parametrize("key, value",
                             [
                                 ("email", "baba_yaga@gmail.com"),
                                 ("name", "Baba Yaga"),
                                 ("password", "qwerty123")
                             ])
    def test_change_auth_user_data_success(self, key, value):
        with allure.step("Подготовить данные нового пользователя"):
            user_data = burgers_api.create_user_body()
            burgers_api.create_user(user_data)
        with allure.step("Авторизоваться и получить токен"):
            body_data = user_data.copy()
            body_data.pop("name", None)
            login_response = burgers_api.login_user(body_data)
            access_token = burgers_api.get_access_token(login_response)
        with allure.step(f"Изменить поле пользователя: {key}"):
            body_data[key] = value
            change_response = burgers_api.change_user_data(access_token, body_data)
        with allure.step("Очистить: удалить пользователя"):
            burgers_api.delete_user(access_token)
        with allure.step("Проверить успешный статус и флаг success"):
            assert change_response.status_code == 200 and change_response.json()["success"] == True

    @allure.title("Проверка невозможности изменения данных пользователя неавторизованным пользователем")
    @allure.description("Неавторизованный пользователь не может редактировать данные пользователя: email, name, password")
    @pytest.mark.parametrize("key, value",
                             [
                                 ("email", "baba_yaga@gmail.com"),
                                 ("name", "Baba Yaga"),
                                 ("password", "qwerty123")
                             ])
    def test_change_not_auth_user_data_fail(self, key, value):
        with allure.step("Подготовить данные нового пользователя"):
            user_data = burgers_api.create_user_body()
            create_response = burgers_api.create_user(user_data)
        with allure.step(f"Сформировать тело запроса на изменение без авторизации: {key}"):
            body_data = user_data.copy()
            body_data[key] = value
        with allure.step("Отправить PATCH без авторизации"):
            change_response = requests.patch(urls.BASE_URL + urls.GET_USER, json=body_data, timeout=7)
        with allure.step("Очистить: удалить созданного пользователя"):
            access_token = burgers_api.get_access_token(create_response)
            burgers_api.delete_user(access_token)
        with allure.step("Проверить статус 401 и корректное сообщение"):
            assert change_response.status_code == 401 and change_response.json()["message"] == data.NOT_AUTHORIZED_MSG