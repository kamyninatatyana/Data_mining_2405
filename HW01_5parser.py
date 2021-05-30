# ДЗ к Уроку 1

# Источник: https://5ka.ru/special_offers/
# Задача организовать сбор данных,
# необходимо иметь метод сохранения данных в .json файлы
# результат: Данные скачиваются с источника, при вызове метода/функции сохранения в файл
# скачанные данные сохраняются в Json файлы, для каждой категории товаров должен быть создан отдельный файл
# и содержать товары исключительно соответсвующие данной категории.
# пример структуры данных для файла:
# нейминг ключей можно делать отличным от примера

# {
# "name": "имя категории",
# "code": "Код соответсвующий категории (используется в запросах)",
# "products": [{PRODUCT}, {PRODUCT}........] # список словарей товаров соответсвующих данной категории
# }"""

import requests
import time
import json
import os

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
}

base_url = 'https://5ka.ru/api/v2/special_offers/'
category_url = 'https://5ka.ru/api/v2/categories/'
product_url = 'https://5ka.ru/api/v2/special_offers/'


def _get_response(url):
    while True:
        response = requests.get(url, headers=headers)
        if response.ok:
            return response
        time.sleep(0.2)


categories = _get_response(category_url).json()
category_list = []
for item in categories:
    category_list.append(item['parent_group_code'])


for group_number in category_list:

    params = f"?categories={group_number}"
    product_url = f"{base_url}{params}"

    while product_url:
        data = _get_response(product_url).json()
        product_url = data['next']
        if not os.path.isdir(group_number):
            os.mkdir(group_number)
            path = os.getcwd()
            for product in data['results']:
                with open(rf'{path}\{group_number}\{product["id"]}.json', "w") as every_product_file:
                    json.dump(product, every_product_file, ensure_ascii=False)
                    print(f'Создан файл {product["id"]}')
            try:
                os.rmdir(rf'{path}\{group_number}')
            except OSError:
                continue
