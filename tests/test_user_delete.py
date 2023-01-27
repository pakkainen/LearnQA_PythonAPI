import pytest
from lib.my_requests import MyRequests
from lib.base_case import BaseCase
from lib.assertions import Assertions


class TestUserDelete(BaseCase):
    def test_delete_test_user(self):
        data = {
            'email': 'vinkotov@example.com',
            'password': '1234'
        }

        # LOGIN TEST-USER
        response1 = MyRequests.post('/user/login', data=data)

        auth_sid = self.get_cookie(response1, 'auth_sid')
        token = self.get_header(response1, 'x-csrf-token')
        user_id = self.get_json_value(response1, 'user_id')

        # DELETE
        response2 = MyRequests.delete(f'/user/{user_id}',
                                      headers={'x-csrf-token': token},
                                      cookies={'auth_sid': auth_sid}
                                      )

        Assertions.assert_code_status(response2, 400)
        assert response2.content.decode('utf-8') == 'Please, do not delete test users with ID 1, 2, 3, 4 or 5.', \
            f"Unexpected response result {response2.content}"

        # CHECK
        response3 = MyRequests.get(f'/user/{user_id}',
                                   headers={'x-csrf-token': token},
                                   cookies={'auth_sid': auth_sid}
                                   )

        Assertions.assert_code_status(response3, 200)

    def test_delete_just_create_user(self):
        # REGISTER
        register_data = self.prepare_registration_data()
        response1 = MyRequests.post("/user/", data=register_data)

        Assertions.assert_code_status(response1, 200)
        Assertions.assert_json_has_key(response1, 'id')

        email = register_data['email']
        password = register_data['password']

        # LOGIN
        data = {
            'email': email,
            'password': password
        }
        response2 = MyRequests.post('/user/login', data=data)

        auth_sid = self.get_cookie(response2, 'auth_sid')
        token = self.get_header(response2, 'x-csrf-token')
        user_id = self.get_json_value(response2, 'user_id')

        # DELETE
        response3 = MyRequests.delete(f'/user/{user_id}',
                                      headers={'x-csrf-token': token},
                                      cookies={'auth_sid': auth_sid}
                                      )

        Assertions.assert_code_status(response3, 200)

        # CHECK
        response4 = MyRequests.get(f'/user/{user_id}',
                                   headers={'x-csrf-token': token},
                                   cookies={'auth_sid': auth_sid}
                                   )

        Assertions.assert_code_status(response4, 404)

    def test_delete_just_create_user_by_another_user(self):
        # REGISTER
        register_data = self.prepare_registration_data()
        response1 = MyRequests.post("/user/", data=register_data)

        Assertions.assert_code_status(response1, 200)
        Assertions.assert_json_has_key(response1, 'id')

        user_id = self.get_json_value(response1, 'id')

        # LOGIN BY TEST USER
        data = {
            'email': 'vinkotov@example.com',
            'password': '1234'
        }
        response2 = MyRequests.post('/user/login', data=data)

        auth_sid = self.get_cookie(response2, 'auth_sid')
        token = self.get_header(response2, 'x-csrf-token')

        # DELETE CREATED USER
        response3 = MyRequests.delete(f'/user/{user_id}',
                                      headers={'x-csrf-token': token},
                                      cookies={'auth_sid': auth_sid}
                                      )

        Assertions.assert_code_status(response3, 400)

        # CHECK
        response4 = MyRequests.get(f'/user/{user_id}',
                                   headers={'x-csrf-token': token},
                                   cookies={'auth_sid': auth_sid}
                                   )

        Assertions.assert_code_status(response4, 200)


