# 1. Посмотреть документацию к API GitHub, разобраться как вывести список репозиториев
# для конкретного пользователя, сохранить JSON-вывод в файле *.json.
import requests

api_url = "https://api.github.com"
user_name = "vsokol"
repos_url = f"{api_url}/users/{user_name}/repos"

response = requests.get(repos_url)
print(f"Для пользователя '{user_name}' доступны следующие публичные репозитории:")
for repos_info in list(response.json()):
    print(repos_info.get("name"))
