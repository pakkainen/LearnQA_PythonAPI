import sys
import time
import requests
import json


def state_check(obj):
    if 'status' in obj:
        print(obj['status'])
        if obj['status'] == 'Job is ready' and 'result' in obj:
            print("Job result:", obj['result'])
    elif 'error' in obj:
        print(obj['error'])
        sys.exit()
    else:
        print('Warning! Unexpected server response')


url = "https://playground.learnqa.ru/ajax/api/longtime_job"
response1 = requests.get(url)  # запрос токена и времени до завершения задачи
param = {"token": response1.json()['token']}
# param = {"token": 'incorrect_token'}  # тест реакции на неверный токен
seconds = response1.json()['seconds']

response2 = requests.get(url, params=param)  # запрос статуса задачи до ее завершения
obj = json.loads(response2.text)
state_check(obj)
time.sleep(seconds)

response3 = requests.get(url, params=param)  # запрос статуса задачи после ее завершения
obj = json.loads(response3.text)
state_check(obj)
