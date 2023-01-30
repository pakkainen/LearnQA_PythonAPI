import pytest
import allure
from lib.my_requests import MyRequests
from lib.base_case import BaseCase
from lib.assertions import Assertions


@allure.feature("Authorization cases")
class TestUserAuth(BaseCase):
    exclude_params = [
        'no_cookie',
        'no_token'
    ]

    def setup_method(self):
        data = {
            'email': 'vinkotov@example.com',
            'password': '1234'
        }

        response1 = MyRequests.post("/user/login", data=data)

        self.auth_sid = self.get_cookie(response1, "auth_sid")
        self.token = self.get_header(response1, "x-csrf-token")
        self.user_id_from_auth_method = self.get_json_value(response1, "user_id")

    @allure.id(1)
    @allure.title('Check the authorization of an existing user')
    @allure.description('This test successfully authorized user by email and password')
    @allure.severity('blocker')  # blocker, critical, normal, minor, trivial
    def test_auth_user(self):
        response2 = MyRequests.get(
            '/user/auth',
            headers={'x-csrf-token': self.token},
            cookies={'auth_sid': self.auth_sid}
        )

        Assertions.assert_json_value_by_name(
            response2,
            "user_id",
            self.user_id_from_auth_method,
            "User id from auth method is not equal to user id from check method"
        )

    @allure.id(2)
    @allure.title('Check authorization failure of a user with {condition}')
    @allure.description(f"This test checks authorization status w/o sending cookie or token")
    @allure.severity('critical')  # blocker, critical, normal, minor, trivial
    @pytest.mark.parametrize('condition', exclude_params)
    def test_negative_auth_check(self, condition):
        if condition == 'no_cookie':
            response2 = MyRequests.get(
                '/user/auth',
                headers={'x-csrf-token': self.token}
            )
            """Send request without cookie"""
        else:
            response2 = MyRequests.get(
                '/user/auth',
                headers={'auth_sid': self.auth_sid}
            )
            """Send request without token"""

        Assertions.assert_json_value_by_name(
            response2,
            "user_id",
            0,
            f"User is authorized with condition {condition}"
        )

