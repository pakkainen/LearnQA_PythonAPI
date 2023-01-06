import requests

response = requests.get("https://playground.learnqa.ru/api/long_redirect", headers={
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:32.0) Gecko/20100101 Firefox/32.0'})
print(f"Произошло {len(response.history)} редиректа")
print("Итоговый URL:", response.url)
print("Код ответа:", response.status_code)