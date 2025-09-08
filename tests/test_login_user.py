import allure
import burgers_api
import pytest
import data


class TestLoginUser:
    @allure.title("Успешная авторизация существующего пользователя")
    @allure.description("Авторизация с email и password в теле запроса")
    def test_login_user_success(self):
        with allure.step("Подготовить данные пользователя"):
            user_data = burgers_api.create_user_body()
        with allure.step("Создать пользователя"):
            user_response = burgers_api.create_user(user_data)
        with allure.step("Подготовить данные для авторизации (без имени)"):
            user_data.pop("name", None)
        with allure.step("Авторизоваться с подготовленными данными"):
            login_response = burgers_api.login_user(user_data)
        with allure.step("Очистить: удалить созданного пользователя"):
            access_token = burgers_api.get_access_token(user_response)
            burgers_api.delete_user(access_token)
        with allure.step("Проверить успешный статус и флаг success"):
            assert login_response.status_code == 200 and login_response.json()["success"] == True

    @allure.title("Проверка возникновения ошибки при попытке авторизоваться с неверными данными")
    @allure.description("Проверка возвращения ошибки при авторизации с неверными email и password")
    @pytest.mark.parametrize("key, value",
                             [
                                 ("email", "wrong_email@test.com"),
                                 ("password", "wrong_password123")
                             ])
    def test_login_with_incorrect_credentials_fail(self, key, value):
        with allure.step("Подготовить корректные данные пользователя"):
            user_data = burgers_api.create_user_body()
        with allure.step("Создать пользователя"):
            user_response = burgers_api.create_user(user_data)
        with allure.step(f"Сформировать данные для авторизации с неверным полем: {key}"):
            login_data = user_data.copy()
            login_data[key] = value
            login_data.pop("name", None)
        with allure.step("Попробовать авторизоваться с неверными данными"):
            login_response = burgers_api.login_user(login_data)
        with allure.step("Очистить: удалить созданного пользователя"):
            access_token = burgers_api.get_access_token(user_response)
            burgers_api.delete_user(access_token)
        with allure.step("Проверить статус 401 и корректное сообщение об ошибке"):
            assert login_response.status_code == 401 and login_response.json()["message"] == data.INCORRECT_DATA_MSG
