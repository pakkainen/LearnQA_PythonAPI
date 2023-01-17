import requests


class TestHeaders:
    def test_headers_value(self):
        url = "https://playground.learnqa.ru/api/homework_header"
        response = requests.get(url)
        print(response.headers.get)
        header_value = response.headers.get('x-secret-homework-header')
        expected_header_value = 'Some secret value'
        assert header_value == expected_header_value, f"Received cookie value does not match expected value" \
                                                      f" '{expected_header_value}'"
