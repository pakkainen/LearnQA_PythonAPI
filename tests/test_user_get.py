import allure

from lib.my_requests import MyRequests
from lib.base_case import BaseCase
from lib.assertions import Assertions


@allure.epic("Getting user info cases")
class TestUserGet(BaseCase):
    @allure.title('Check to GET username from user id')
    @allure.description("This test checks that the unauthorized user can GET username from a user id")
    def test_get_user_details_not_auth(self):
        response = MyRequests.get("/user/2")

        unexpected_fields = ['email', 'firstName', 'lastName']
        Assertions.assert_json_has_unfamiliar_user_key(response, 'username', unexpected_fields)

    @allure.title('Check to GET user info by himself')
    @allure.description("This test checks that the authorized user"
                        " can GET his info (username, email, firstName, lastName)")
    def test_get_user_details_auth_as_same_user(self):
        data = {
            'email': 'vinkotov@example.com',
            'password': '1234'
        }

        response1 = MyRequests.post('/user/login', data=data)

        auth_sid = self.get_cookie(response1, 'auth_sid')
        token = self.get_header(response1, "x-csrf-token")
        user_id_from_auth_method = self.get_json_value(response1, "user_id")

        response2 = MyRequests.get(f"/user/{user_id_from_auth_method}",
                                   headers={'x-csrf-token': token},
                                   cookies={"auth_sid": auth_sid}
                                   )

        expected_fields = ['username', 'email', 'firstName', 'lastName']
        Assertions.assert_json_has_keys(response2, expected_fields)

    @allure.title('Checking authorized user access only to username of another user')
    @allure.description("This test checks that the authorized user can only GET username from another user id")
    def test_get_user_details_auth_as_another_user(self):
        data = {
            'email': 'vinkotov@example.com',
            'password': '1234'
        }

        response1 = MyRequests.post('/user/login', data=data)

        auth_sid = self.get_cookie(response1, 'auth_sid')
        token = self.get_header(response1, "x-csrf-token")

        response2 = MyRequests.get("/user/1",
                                   headers={'x-csrf-token': token},
                                   cookies={"auth_sid": auth_sid}
                                   )

        unexpected_fields = ['email', 'firstName', 'lastName']
        Assertions.assert_json_has_unfamiliar_user_key(response2, 'username', unexpected_fields)
