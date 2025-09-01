import pytest
import burgers_api

@pytest.fixture(scope='function')
def default_user():
    user_body = burgers_api.create_user_body()
    user_response = burgers_api.create_user(user_body)
    access_token = burgers_api.get_access_token(user_response)
    yield user_response, access_token
    burgers_api.delete_user(access_token)

@pytest.fixture(scope='function')
def default_burger():
    ingredients = burgers_api.get_ingredients().json()
    ingredient_types = {"main": None, "sauce": None, "bun": None}
    for item in ingredients["data"]:
        if item["type"] in ingredient_types and ingredient_types[item["type"]] is None:
            ingredient_types[item["type"]] = item["_id"]
    burger_ingredient = {"ingredients": list(ingredient_types.values())}
    return burger_ingredient

