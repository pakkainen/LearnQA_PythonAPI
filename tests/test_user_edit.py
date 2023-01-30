import allure

from lib.my_requests import MyRequests
from lib.base_case import BaseCase
from lib.assertions import Assertions


@allure.feature("User editing cases")
class TestUserEdit(BaseCase):
    @allure.id(12)
    @allure.title('Check just created user editing by himself')
    @allure.description("This test checks that the just created user can be edited by himself")
    @allure.severity('blocker')  # blocker, critical, normal, minor, trivial
    def test_edit_just_create_user(self):
        # REGISTER
        register_data = self.prepare_registration_data()
        response1 = MyRequests.post("/user/", data=register_data)

        Assertions.assert_code_status(response1, 200)
        Assertions.assert_json_has_key(response1, 'id')

        email = register_data['email']
        password = register_data['password']
        user_id = self.get_json_value(response1, 'id')

        # LOGIN
        login_data = {
            'email': email,
            'password': password
        }
        response2 = MyRequests.post('/user/login', data=login_data)

        auth_sid = self.get_cookie(response2, 'auth_sid')
        token = self.get_header(response2, 'x-csrf-token')

        # EDIT
        new_name = "Changed Name"
        response3 = MyRequests.put(f"/user/{user_id}",
                                   headers={'x-csrf-token': token},
                                   cookies={'auth_sid': auth_sid},
                                   data={'firstName': new_name}
                                   )

        Assertions.assert_code_status(response3, 200)

        # GET
        response4 = MyRequests.get(f"/user/{user_id}",
                                   headers={'x-csrf-token': token},
                                   cookies={'auth_sid': auth_sid}
                                   )

        Assertions.assert_json_value_by_name(response4, 'firstName', new_name, "Wrong name of user after edit")

    @allure.id(13)
    @allure.title('Check just created user editing failure by unauthorized user')
    @allure.description("This test checks that the just created user can't be edited by unauthorized user")
    @allure.severity('critical')  # blocker, critical, normal, minor, trivial
    def test_edit_just_create_user_by_unauthorized_user(self):
        # REGISTER
        register_data = self.prepare_registration_data()
        response1 = MyRequests.post("/user/", data=register_data)

        Assertions.assert_code_status(response1, 200)
        Assertions.assert_json_has_key(response1, 'id')

        user_id = self.get_json_value(response1, 'id')

        # EDIT
        new_name = "Changed Name"
        for key in ('username', 'firstName', 'lastName'):
            response2 = MyRequests.put(f"/user/{user_id}", data={key: new_name})

            Assertions.assert_code_status(response2, 400)
            assert response2.content.decode("utf-8") == f"Auth token not supplied", \
                f"Unexpected response result {response2.content}"

    @allure.id(14)
    @allure.title('Check just created user editing failure by another user')
    @allure.description("This test checks that the just created user can't be edited by another user")
    @allure.severity('critical')  # blocker, critical, normal, minor, trivial
    def test_edit_just_create_user_by_another_user(self):
        # REGISTER_TEST_USER
        register_data = self.prepare_registration_data()
        response1 = MyRequests.post("/user/", data=register_data)

        Assertions.assert_code_status(response1, 200)
        Assertions.assert_json_has_key(response1, 'id')

        test_user_username = register_data['username']
        test_user_id = self.get_json_value(response1, 'id')

        # REGISTER_EDITOR
        register_data = self.prepare_registration_data()
        response2 = MyRequests.post("/user/", data=register_data)

        Assertions.assert_code_status(response2, 200)
        Assertions.assert_json_has_key(response2, 'id')

        email = register_data['email']
        password = register_data['password']

        # LOGIN_EDITOR
        login_data = {
            'email': email,
            'password': password
        }
        response3 = MyRequests.post('/user/login', data=login_data)

        editor_auth_sid = self.get_cookie(response3, 'auth_sid')
        editor_token = self.get_header(response3, 'x-csrf-token')

        # EDIT_TEST_USER
        response4 = MyRequests.put(f"/user/{test_user_id}",
                                   headers={'x-csrf-token': editor_token},
                                   cookies={'auth_sid': editor_auth_sid},
                                   data={'username': 'ChangedName'}
                                   )

        Assertions.assert_code_status(response4, 200)

        # GET_TEST_USER
        response5 = MyRequests.get(f"/user/{test_user_id}",
                                   headers={'x-csrf-token': editor_token},
                                   cookies={'auth_sid': editor_auth_sid}
                                   )

        Assertions.assert_json_value_by_name(response5, 'username', test_user_username,
                                             'Registered user can edit unregistered user')

    @allure.id(15)
    @allure.title('Check failure to change email to new one without at')
    @allure.description("This test checks that the just created user can't change email to a new one without @")
    @allure.severity('critical')  # blocker, critical, normal, minor, trivial
    def test_edit_authorized_user_email_without_at(self):
        # REGISTER
        register_data = self.prepare_registration_data()
        response1 = MyRequests.post("/user/", data=register_data)

        Assertions.assert_code_status(response1, 200)
        Assertions.assert_json_has_key(response1, 'id')

        email = register_data['email']
        password = register_data['password']
        user_id = self.get_json_value(response1, 'id')

        # LOGIN
        login_data = {
            'email': email,
            'password': password
        }
        response2 = MyRequests.post('/user/login', data=login_data)

        auth_sid = self.get_cookie(response2, 'auth_sid')
        token = self.get_header(response2, 'x-csrf-token')

        # EDIT
        invalid_email = email.replace('@', '')
        response3 = MyRequests.put(f"/user/{user_id}",
                                   headers={'x-csrf-token': token},
                                   cookies={'auth_sid': auth_sid},
                                   data={'email': invalid_email}
                                   )

        Assertions.assert_code_status(response3, 400)
        assert response3.content.decode("utf-8") == f"Invalid email format", \
            f"Unexpected response result {response3.content}"

        # GET
        response4 = MyRequests.get(f"/user/{user_id}",
                                   headers={'x-csrf-token': token},
                                   cookies={'auth_sid': auth_sid}
                                   )

        Assertions.assert_json_value_by_name(response4, 'email', email,
                                             f"The user's email has been changed to an invalid email: {invalid_email}")

    @allure.id(16)
    @allure.title('Check failure to change name to one symbol')
    @allure.description("This test checks that the just created user can't change his name to one symbol")
    @allure.severity('normal')  # blocker, critical, normal, minor, trivial
    def test_edit_authorized_user_firstname_to_one_symbol(self):
        # REGISTER
        register_data = self.prepare_registration_data()
        response1 = MyRequests.post("/user/", data=register_data)

        Assertions.assert_code_status(response1, 200)
        Assertions.assert_json_has_key(response1, 'id')

        email = register_data['email']
        first_name = register_data['firstName']
        password = register_data['password']
        user_id = self.get_json_value(response1, 'id')

        # LOGIN
        login_data = {
            'email': email,
            'password': password
        }
        response2 = MyRequests.post('/user/login', data=login_data)

        auth_sid = self.get_cookie(response2, 'auth_sid')
        token = self.get_header(response2, 'x-csrf-token')

        # EDIT
        short_name = "a"
        response3 = MyRequests.put(f"/user/{user_id}",
                                   headers={'x-csrf-token': token},
                                   cookies={'auth_sid': auth_sid},
                                   data={'firstName': short_name}
                                   )

        Assertions.assert_code_status(response3, 400)
        assert response3.json()['error'] == 'Too short value for field firstName', \
            f"Unexpected response result {response3.content}"

        # GET
        response4 = MyRequests.get(f"/user/{user_id}",
                                   headers={'x-csrf-token': token},
                                   cookies={'auth_sid': auth_sid}
                                   )

        Assertions.assert_json_value_by_name(
            response4,
            'firstName',
            first_name,
            f"The user can change their name to a name that is too short: {short_name}"
        )
