# 2. Изучить список открытых API. Найти среди них любое, требующее авторизацию (любого типа).
# Выполнить запросы к нему, пройдя авторизацию. Ответ сервера записать в файл.
import requests
import json
from pprint import pprint

url = 'https://suggestions.dadata.ru/suggestions/api/4_1/rs/findById/bank'
token = '335cef2bd28f8fbfd041e9d205843c5fe3a2f3cd'
headers = {'Content-Type': 'application/json',
           'Accept': 'application/json', 'Authorization': f'Token {token}'}

bank_inn = '044525225'
# bank_inn = '04452522554'

res = requests.post(url, data=json.dumps({'query': bank_inn}), headers=headers)
if res.ok:
    with open('bank.json', 'w') as file:
        json.dump(res.json(), file)

    print(f"Информация по банку с ИНН = {bank_inn}")
    pprint(dict(res.json()))
