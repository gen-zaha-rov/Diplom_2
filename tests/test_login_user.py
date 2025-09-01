import allure
import burgers_api
import pytest
import data


class TestLoginUser:
    @allure.title("Успешная авторизация существующего пользователя")
    @allure.description("Авторизация с email и password в теле запроса")
    def test_login_user_success(self):
        user_data = burgers_api.create_user_body()
        user_response = burgers_api.create_user(user_data)
        user_data.pop("name", None)
        login_response = burgers_api.login_user(user_data)
        access_token = burgers_api.get_access_token(user_response)
        burgers_api.delete_user(access_token)
        assert login_response.status_code == 200 and login_response.json()["success"] == True

    @allure.title("Проверка возникновения ошибки при попытке авторизоваться с неверными данными")
    @allure.description("Проверка возвращения ошибки при авторизации с неверными email и password")
    @pytest.mark.parametrize("key, value",
                             [
                                 ("email", "wrong_email@test.com"),
                                 ("password", "wrong_password123")
                             ])
    def test_login_with_incorrect_credentials_fail(self, key, value):
        user_data = burgers_api.create_user_body()
        user_response = burgers_api.create_user(user_data)
        login_data = user_data.copy()
        login_data[key] = value
        login_data.pop("name", None)
        login_response = burgers_api.login_user(login_data)
        access_token = burgers_api.get_access_token(user_response)
        burgers_api.delete_user(access_token)
        assert login_response.status_code == 401 and login_response.json()["message"] == data.INCORRECT_DATA_MSG
