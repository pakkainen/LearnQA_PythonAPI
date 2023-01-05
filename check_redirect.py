import requests

response = requests.get("https://playground.learnqa.ru/api/long_redirect")
print(f"Произошло {len(response.history)} редиректа")
print("Итоговый URL:", response.history[-1].url)