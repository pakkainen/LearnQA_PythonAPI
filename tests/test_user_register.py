import string
import random
import pytest
from lib.my_requests import MyRequests
from lib.base_case import BaseCase
from lib.assertions import Assertions


class TestUserRegister(BaseCase):
    def test_create_user_successfully(self):
        data = self.prepare_registration_data()

        response = MyRequests.post("/user/", data=data)

        Assertions.assert_code_status(response, 200)
        Assertions.assert_json_has_key(response, "id")

    def test_create_user_with_existing_email(self):
        email = 'vinkotov@example.com'
        data = self.prepare_registration_data(email)

        response = MyRequests.post("/user/", data=data)

        Assertions.assert_code_status(response, 400)
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

        response = MyRequests.post("/user/", data=data)

        Assertions.assert_code_status(response, 400)
        assert response.content.decode("utf-8") == f"Invalid email format", \
            f"Unexpected response content {response.content}"

    @pytest.mark.parametrize("exclude_param", ['username', 'password', 'firstName', 'lastName', 'email'])
    def test_create_user_without_required_field(self, exclude_param):
        data = self.prepare_registration_data()
        del data[exclude_param]

        response = MyRequests.post("/user/", data=data)

        Assertions.assert_code_status(response, 400)
        assert response.content.decode("utf-8") == f"The following required params are missed: {exclude_param}", \
            f"Unexpected response content {response.content}"

    @pytest.mark.parametrize("short_name", ['username', 'firstName', 'lastName'])
    def test_create_user_with_short_name(self, short_name):
        data = self.prepare_registration_data()
        data[short_name] = ''.join(random.choices(string.ascii_letters + string.digits, k=1))

        response = MyRequests.post("/user/", data=data)

        Assertions.assert_code_status(response, 400)
        assert response.content.decode("utf-8") == f"The value of '{short_name}' field is too short", \
            f"Unexpected response content {response.content}"

    @pytest.mark.parametrize("long_name", ['username', 'firstName', 'lastName'])
    def test_create_user_with_long_name(self, long_name):
        data = self.prepare_registration_data()
        data[long_name] = ''.join(random.choices(string.ascii_letters + string.digits, k=random.randint(251, 300)))

        response = MyRequests.post("/user/", data=data)

        Assertions.assert_code_status(response, 400)
        assert response.content.decode("utf-8") == f"The value of '{long_name}' field is too long", \
            f"Unexpected response content {response.content}"
