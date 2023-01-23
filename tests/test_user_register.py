from datetime import datetime

import string
import random
import pytest
import requests
from lib.base_case import BaseCase
from lib.assertions import Assertions

class TestUserRegister(BaseCase):
    def setup_method(self):
        base_part = 'learnqa'
        domain = 'example.com'
        random_part = datetime.now().strftime("%m%d%Y%H%M%S")
        self.email = f"{base_part}{random_part}@{domain}"

    def test_create_user_successfully(self):
        data = {
            'password': '123',
            'username': 'learnqa',
            'firstName': 'learnqa',
            'lastName': 'learnqa',
            'email': self.email
        }

        response = requests.post("https://playground.learnqa.ru/api/user/", data=data)

        Assertions.asset_code_status(response, 200)
        Assertions.assert_json_has_key(response, "id")

    def test_create_user_with_existing_email(self):
        email = 'vinkotov@example.com'
        data = {
            'password': '123',
            'username': 'learnqa',
            'firstName': 'learnqa',
            'lastName': 'learnqa',
            'email': email
        }

        response = requests.post("https://playground.learnqa.ru/api/user/", data=data)

        Assertions.asset_code_status(response, 400)
        assert response.content.decode("utf-8") == f"Users with email '{email}' already exists", \
            f"Unexpected response content {response.content}"

    def test_create_user_with_email_without_at(self):
        email = 'userexample.com'
        data = {
            'password': '123',
            'username': 'learnqa',
            'firstName': 'learnqa',
            'lastName': 'learnqa',
            'email': email
        }

        response = requests.post("https://playground.learnqa.ru/api/user/", data=data)

        Assertions.asset_code_status(response, 400)
        assert response.content.decode("utf-8") == f"Invalid email format", \
            f"Unexpected response content {response.content}"

    @pytest.mark.parametrize("exclude_param", ['username', 'password', 'firstName', 'lastName', 'email'])
    def test_create_user_without_required_field(self, exclude_param):
        data = {
            'password': '123',
            'username': 'learnqa',
            'firstName': 'learnqa',
            'lastName': 'learnqa',
            'email': self.email
        }
        del data[exclude_param]

        response = requests.post("https://playground.learnqa.ru/api/user/", data=data)

        Assertions.asset_code_status(response, 400)
        assert response.content.decode("utf-8") == f"The following required params are missed: {exclude_param}", \
            f"Unexpected response content {response.content}"

    @pytest.mark.parametrize("short_name", ['username', 'firstName', 'lastName'])
    def test_create_user_with_short_name(self, short_name):
        data = {
            'password': '123',
            'username': 'learnqa',
            'firstName': 'learnqa',
            'lastName': 'learnqa',
            'email': self.email,
            short_name: ''.join(random.choices(string.ascii_letters + string.digits, k=1))
        }

        response = requests.post("https://playground.learnqa.ru/api/user/", data=data)

        Assertions.asset_code_status(response, 400)
        assert response.content.decode("utf-8") == f"The value of '{short_name}' field is too short", \
            f"Unexpected response content {response.content}"

    @pytest.mark.parametrize("long_name", ['username', 'firstName', 'lastName'])
    def test_create_user_with_long_name(self, long_name):
        data = {
            'password': '123',
            'username': 'learnqa',
            'firstName': 'learnqa',
            'lastName': 'learnqa',
            'email': self.email,
            long_name: ''.join(random.choices(string.ascii_letters + string.digits, k=random.randint(251, 300)))
        }

        response = requests.post("https://playground.learnqa.ru/api/user/", data=data)

        Assertions.asset_code_status(response, 400)
        assert response.content.decode("utf-8") == f"The value of '{long_name}' field is too long", \
            f"Unexpected response content {response.content}"
