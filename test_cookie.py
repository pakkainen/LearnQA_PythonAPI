import requests


class TestCookie:
    def test_cookie_value(self):
        url = "https://playground.learnqa.ru/api/homework_cookie"
        response = requests.get(url)
        cookie_value = response.cookies.get('HomeWork')
        expected_cookie_value = 'hw_value'
        assert cookie_value == expected_cookie_value, f"Received cookie value does not match expected value" \
                                                      f" '{expected_cookie_value}'"
