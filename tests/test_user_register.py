import string
import random
import pytest
import allure
from lib.my_requests import MyRequests
from lib.base_case import BaseCase
from lib.assertions import Assertions


@allure.feature("Registration cases")
class TestUserRegister(BaseCase):
    @allure.id(3)
    @allure.title('Check test user registration')
    @allure.severity('blocker')  # blocker, critical, normal, minor, trivial
    def test_create_user_successfully(self):
        data = self.prepare_registration_data()

        response = MyRequests.post("/user/", data=data)

        Assertions.assert_code_status(response, 200)
        Assertions.assert_json_has_key(response, "id")

    @allure.id(4)
    @allure.severity('critical')  # blocker, critical, normal, minor, trivial
    @allure.title('Check test registration failure for existing email')
    def test_create_user_with_existing_email(self):
        email = 'vinkotov@example.com'
        data = self.prepare_registration_data(email)

        response = MyRequests.post("/user/", data=data)

        Assertions.assert_code_status(response, 400)
        assert response.content.decode("utf-8") == f"Users with email '{email}' already exists", \
            f"Unexpected response content {response.content}"

    @allure.id(5)
    @allure.title('Check test registration failure for email without at')
    @allure.severity('critical')  # blocker, critical, normal, minor, trivial
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

    @allure.id(6)
    @allure.title('Check test registration failure with empty required fields')
    @allure.severity('critical')  # blocker, critical, normal, minor, trivial
    @pytest.mark.parametrize("exclude_param", ['username', 'password', 'firstName', 'lastName', 'email'])
    def test_create_user_without_required_field(self, exclude_param):
        data = self.prepare_registration_data()
        del data[exclude_param]

        response = MyRequests.post("/user/", data=data)

        Assertions.assert_code_status(response, 400)
        assert response.content.decode("utf-8") == f"The following required params are missed: {exclude_param}", \
            f"Unexpected response content {response.content}"

    @allure.id(7)
    @allure.title('Check test registration failure for short name')
    @allure.severity('normal')  # blocker, critical, normal, minor, trivial
    @pytest.mark.parametrize("short_name", ['username', 'firstName', 'lastName'])
    def test_create_user_with_short_name(self, short_name):
        data = self.prepare_registration_data()
        data[short_name] = ''.join(random.choices(string.ascii_letters + string.digits, k=1))

        response = MyRequests.post("/user/", data=data)

        Assertions.assert_code_status(response, 400)
        assert response.content.decode("utf-8") == f"The value of '{short_name}' field is too short", \
            f"Unexpected response content {response.content}"

    @allure.id(8)
    @allure.title('Check test registration failure for long name')
    @allure.severity('normal')  # blocker, critical, normal, minor, trivial
    @pytest.mark.parametrize("long_name", ['username', 'firstName', 'lastName'])
    def test_create_user_with_long_name(self, long_name):
        data = self.prepare_registration_data()
        data[long_name] = ''.join(random.choices(string.ascii_letters + string.digits, k=random.randint(251, 300)))

        response = MyRequests.post("/user/", data=data)

        Assertions.assert_code_status(response, 400)
        assert response.content.decode("utf-8") == f"The value of '{long_name}' field is too long", \
            f"Unexpected response content {response.content}"
