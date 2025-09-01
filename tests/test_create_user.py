import allure
import burgers_api
import data
from helpers import ChangeTestDataHelper
import pytest


class TestCreateUser:
    @allure.title("Проверить успешную регистрацию пользователя")
    @allure.description("Создать пользователя. Проверить статус и тело ответа")
    def test_create_user_success(self, default_user):
        user_response, access_token = default_user
        #assert user_response.status_code == 200 and user_response.json() is not None
        assert user_response.status_code == 200
        assert user_response.json() is not None
        assert "user" in user_response.json()
        assert "email" in user_response.json()["user"]

    @allure.title("Ошибка 403 при попытке создания уже существующего пользователя")
    @allure.description("Создание уже существующего пользователя. Проверка статуса и тела ответа")
    def test_duplicate_user_fail(self):
        body = burgers_api.create_user_body()
        user_response = burgers_api.create_user(body)
        create_duplicate_request = burgers_api.create_user(body)
        access_token = burgers_api.get_access_token(user_response)
        burgers_api.delete_user(access_token)
        assert create_duplicate_request.status_code == 403 and create_duplicate_request.json()["message"] == data.DUPLICATE_USER_MSG

    @allure.title("Ошибка 403 при попытке создания пользователя без одного из обязательных полей: email, password, name")
    @allure.description("Отправить запрос на создание пользователя без заполнения обязательного поля и получить ошибку 403")
    @pytest.mark.parametrize('key, value',[
                                 ("email", ""),
                                 ("password", ""),
                                 ("name", "")
                             ])
    def test_create_user_without_field_fail(self, key, value):
        body = ChangeTestDataHelper.modify_create_user_body(key, value)
        user_response = burgers_api.create_user(body)
        assert user_response.status_code == 403 and user_response.json()["message"] == data.EMPTY_REQUIRED_FIELD_MSG