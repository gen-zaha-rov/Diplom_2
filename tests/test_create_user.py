import allure
import burgers_api
import data
from helpers import ChangeTestDataHelper
import pytest


class TestCreateUser:
    @allure.title("Проверить успешную регистрацию пользователя")
    @allure.description("Создать пользователя. Проверить статус и тело ответа")
    def test_create_user_success(self, default_user):
        with allure.step("Создать пользователя через фикстуру"):
            user_response, access_token = default_user
        with allure.step("Проверить, что код ответа равен 200"):
            assert user_response.status_code == 200
        with allure.step("Проверить, что тело ответа не пустое"):
            assert user_response.json() is not None
        with allure.step("Проверить, что тело ответа содержит поле 'user'"):
            assert "user" in user_response.json()
        with allure.step("Проверить, что у пользователя есть поле 'email'"):
            assert "email" in user_response.json()["user"]

    @allure.title("Ошибка 403 при попытке создания уже существующего пользователя")
    @allure.description("Создание уже существующего пользователя. Проверка статуса и тела ответа")
    def test_duplicate_user_fail(self):
        with allure.step("Сформировать тело запроса на создание пользователя"):
            body = burgers_api.create_user_body()
        with allure.step("Создать пользователя"):
            user_response = burgers_api.create_user(body)
        with allure.step("Повторно отправить запрос на создание того же пользователя"):
            create_duplicate_request = burgers_api.create_user(body)
        with allure.step("Получить access_token созданного пользователя"):
            access_token = burgers_api.get_access_token(user_response)
        with allure.step("Удалить созданного пользователя для очистки"):
            burgers_api.delete_user(access_token)
        with allure.step("Проверить, что вернулась ошибка 403 и корректное сообщение"):
            assert create_duplicate_request.status_code == 403 and create_duplicate_request.json()["message"] == data.DUPLICATE_USER_MSG

    @allure.title("Ошибка 403 при попытке создания пользователя без одного из обязательных полей: email, password, name")
    @allure.description("Отправить запрос на создание пользователя без заполнения обязательного поля и получить ошибку 403")
    @pytest.mark.parametrize('key, value',[
                                 ("email", ""),
                                 ("password", ""),
                                 ("name", "")
                             ])
    def test_create_user_without_field_fail(self, key, value):
        with allure.step(f"Подготовить тело запроса без обязательного поля: {key}"):
            body = ChangeTestDataHelper.modify_create_user_body(key, value)
        with allure.step("Отправить запрос на создание пользователя с неполными данными"):
            user_response = burgers_api.create_user(body)
        with allure.step("Проверить, что вернулась ошибка 403 и корректное сообщение"):
            assert user_response.status_code == 403 and user_response.json()["message"] == data.EMPTY_REQUIRED_FIELD_MSG