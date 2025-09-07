import allure
import helpers
import urls
import requests


DEFAULT_TIMEOUT = 7

@allure.step("Сделать тело запроса на создание пользователя: email, password, name")
def create_user_body():
    return helpers.new_user_login_password()

@allure.step("Создать пользователя")
def create_user(user_data):
    user_response = requests.post(urls.BASE_URL+urls.CREATE_USER, json=user_data, timeout=DEFAULT_TIMEOUT)
    return user_response

@allure.step("Получить access token созданного пользователя")
def get_access_token(user_response):
    access_token = user_response.json().get("accessToken")
    return access_token

@allure.step("Удалить созданного пользователя")
def delete_user(access_token):
    headers = {"Authorization": access_token}
    response_delete = requests.delete(urls.BASE_URL + urls.GET_USER, headers=headers, timeout=DEFAULT_TIMEOUT)
    return response_delete

@allure.step("Авторизовать зарегистрированного пользователя")
def login_user(login_data):
    login_response = requests.post(urls.BASE_URL + urls.LOGIN_USER, json=login_data, timeout=DEFAULT_TIMEOUT)
    return login_response

@allure.step("Изменить данные пользователя: email, password, name")
def change_user_data(access_token, new_data):
    headers = {"Authorization": access_token}
    change_data_response = requests.patch(urls.BASE_URL + urls.GET_USER, headers=headers, json=new_data, timeout=DEFAULT_TIMEOUT)
    return change_data_response

@allure.step("Получить refreshtoken созданного пользователя")
def get_refresh_token(user_response):
    refresh_token = user_response.json().get("refreshToken")
    return refresh_token

@allure.step("Получить список доступных ингредиентов")
def get_ingredients():
    response = requests.get(urls.BASE_URL + urls.GET_INGREDIENTS, timeout=DEFAULT_TIMEOUT)
    return response

@allure.step("Создать заказ")
def create_new_order(headers, ingredients):
    response = requests.post(urls.BASE_URL + urls.GET_USER_ORDERS, headers=headers, json=ingredients, timeout=DEFAULT_TIMEOUT)
    return response

@allure.step("Получить все заказы конкретного пользователя")
def get_users_orders(headers):
    response = requests.get(urls.BASE_URL + urls.GET_USER_ORDERS, headers=headers, timeout=DEFAULT_TIMEOUT)
    return response