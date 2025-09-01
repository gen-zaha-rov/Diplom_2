import random
import string


def new_user_login_password():
    def generate_random_string(length):
        letters = string.ascii_lowercase
        random_string = ''.join(random.choice(letters) for i in range(length))
        return random_string

    email = f'{generate_random_string(5)}@gmail.com'
    password = generate_random_string(10)
    name = generate_random_string(10)
    payload = {
        "email": email,
        "password": password,
        "name": name
    }
    return payload

class ChangeTestDataHelper:
    @staticmethod
    def modify_create_user_body(key, value):
        body = new_user_login_password().copy()
        body[key] = value
        return body