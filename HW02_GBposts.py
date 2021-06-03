# ДЗ2
# Источник https://gb.ru/posts/
# Необходимо обойти все записи в блоге и извлечь из них информацию следующих полей:
# url страницы материала
# Заголовок материала
# Первое изображение материала (Ссылка)
# Дата публикации (в формате datetime)
# имя автора материала
# ссылка на страницу автора материала
# комментарии в виде (автор комментария и текст комментария)
# Структуру сохраняем в MongoDB

import requests
from urllib.parse import urljoin
import bs4
import datetime
import time
import pymongo

# 1. Взять стартовую ссылку, получить всю необходимую информацию из первой статьи, сложить в базу данных,
# перейти к следующей статье.
# 2. Получить список страниц.
# 3. Изменить стартовую ссылку на первую страницу в списке страниц. Получить всю необходимую информцию из первой
# статьи на странице, сложить в базу данных, перейти к следующей странице.


class GbBlogParser:

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    }

    def __init__(self, start_url):
        self.start_url = start_url
        self.pagination_list = []
        self.data = {}

    def _get_response(self, url):
        response = requests.get(url, headers=self.headers)
        print(f"RESPONSE: {response.url}")
        return response

    def _get_soup(self, response):
        soup = bs4.BeautifulSoup(response.text, "lxml")
        return soup

    def _get_comment_info(self):
        comment_url = response.url
        comment_response = self._get_response(comment_url)
        comment_soup = self._get_soup(comment_response)



    def parse_post(self, soup):
        posts = soup.find("div", attrs={"class": "post-items-wrapper"})
        author_name_tag = soup.find("div", itemprop="author")

        data = {
            "post_data": {
            "url": response.url,
            "title": soup.find("h1", attrs={"class": "blogpost-title"}).text,
            "image": soup.find("img", attrs={"class": "col-md-12"}).attrs.get('src'),
            "post_date": soup.find("div", attrs={"class": "small m-t-xs"}).text,
            },
            "author_data": {
                "url": urljoin(response.url, author_name_tag.parent.attrs.get("href")),
                "name": author_name_tag.text,
            },
            "tags_data": [
                {"tag_name": tag.text,
                 "url": urljoin(response.url, tag.attrs.get("href"))
                 }
                for tag in soup.find_all("a", attrs={"class": "small"})
            ]



        }
        self._save(data)





    def _get_response(self):
        pass


# if __name__ == '__main__':
#    parser = GbBlogParser('https://gb.ru/posts')
#     parser.run()


url = 'https://gb.ru/posts'
response = requests.get(url)
soup = bs4.BeautifulSoup(response.text, 'lxml')

# Получаем пагинацию

pagination = soup.find("ul", attrs={"class": "gb__pagination"})
pagination_list = []
for a_tag in pagination.find_all("a"):
    if a_tag.attrs.get("href"):
        pagination_list.append(a_tag.attrs.get("href")) #Удалить последний?

print(pagination_list)

# Получаем статьи на странице



headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    }
# Функция которая собирает статьи со страницы и переходит на следующую:

# ef get_posts_from_page(pagination_list):
page_url = urljoin(url, pagination_list.pop(0))
response = requests.get(page_url, headers=headers)
print(page_url)


image = soup.find("img", attrs={"class": "col-md-12"}).attrs.get('src')
print(image)

post_date = soup.find("div", attrs={"class": "small m-t-xs"}).text
# post_date = datetime.date(post_date) Подумать потом
print(post_date)

response = requests.get('https://gb.ru/posts/about-neural-network')
soup = bs4.BeautifulSoup(response.text, 'lxml')
tag_info = soup.find_all("a", attrs={"class": "small"})
print(tag_info)


##################