from json.decoder import JSONDecodeError
import requests


print("\n Запрос без параметра")
response = requests.get("https://playground.learnqa.ru/ajax/api/compare_query_type")
print('Код ответа -', response.status_code, response.text)

print("\n Неподдерживаемый сервером запрос с параметром")
response = requests.head("https://playground.learnqa.ru/ajax/api/compare_query_type", data={"method": "HEAD"})
print('Код ответа -', response.status_code, response.text)

print("\n Запрос с параметром")
response = requests.get("https://playground.learnqa.ru/ajax/api/compare_query_type", params={"method": "GET"})
print('Код ответа -', response.status_code, response.text)

print("\n Цикл: типы запросов + параметры")
method = ("GET", "POST", "PUT", "DELETE")
request = (requests.get, requests.post, requests.put, requests.delete)
for i in request:
    for j in method:
        if request[0]:
            response = i("https://playground.learnqa.ru/ajax/api/compare_query_type", params={"method": j})
        else:
            response = i("https://playground.learnqa.ru/ajax/api/compare_query_type", data={"method": j})
        print('Код ответа -', response.status_code, end=' ')
        try:
            parsed_response_text = response.json()
            if method.index(j) == request.index(i):
                print(parsed_response_text)
            else:
                print('ERROR! Request processed with invalid data: param value is not equal to a method')
        except JSONDecodeError:
            print(response.text)