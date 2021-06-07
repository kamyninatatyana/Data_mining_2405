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
import time
import pymongo


class GbBlogParser:
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    }

    __parse_time = 0

    def __init__(self, start_url, db, delay=1.0):
        self.start_url = start_url
        self.delay = delay
        self.db = db
        self.done_url = set()
        self.tasks = []
        self.task_list({self.start_url, }, self.parse_pagination)

    def _get_response(self, url):
        while True:
            next_apply_time = self.__parse_time + self.delay
            if next_apply_time > time.time():
                time.sleep(next_apply_time - time.time())
            response = requests.get(url, headers=self.headers)
            self.__parse_time = time.time()
            if response.ok:
                return response

    def _get_comment_info(self, commentable_id):
        comment_url = f"api/v2/comments?commentable_type=Post&commentable_id={commentable_id}&order=desc"
        comment_response = self._get_response(urljoin(self.start_url, comment_url))
        comment_info = comment_response.json()
        return comment_info

    def parse_post(self, response):
        soup = bs4.BeautifulSoup(response.text, "lxml")
        author_name_tag = soup.find("div", itemprop="author")

        data = {
            "post_data": {
                "url": response.url,
                "title": soup.find("h1", attrs={"class": "blogpost-title"}).text,
                "post_date": soup.find("time", attrs={"class": "text-md text-muted m-r-md"}).text,
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
            ],
            "comments_info": self._get_comment_info(soup.find("comments").attrs.get("commentable-id")),
        }
        self._save(data)

    def parse_pagination(self, response):
        soup = bs4.BeautifulSoup(response.text, "lxml")

        pagination = soup.find("ul", attrs={"class": "gb__pagination"})
        self.task_list(
            {
                urljoin(response.url, a_tag.attrs["href"])
                for a_tag in pagination.find_all("a")
                if a_tag.attrs.get("href")
            },
            self.parse_pagination,
        )
        post_wrapper = soup.find("div", attrs={"class": "post-items-wrapper"})
        self.task_list(
            {
                urljoin(response.url, a_tag.attrs["href"])
                for a_tag in post_wrapper.find_all("a", attrs={"class": "post-item__title"})
                if a_tag.attrs.get("href")
            },
            self.parse_post,
        )

    def task_list(self, urls, callback):
        urls_set = urls - self.done_url
        for url in urls_set:
            self.tasks.append(self.get_task(url, callback))
            self.done_url.add(url)

    def get_task(self, url, callback):
        def task():
            response = self._get_response(url)
            return callback(response)

        return task

    def run(self):
        while True:
            try:
                task = self.tasks.pop(0)
                task()
            except IndexError:
                break

    def _save(self, data):
        collection = self.db["Data_mining_HW2"]["GB_blogs_collection"]
        collection.insert_one(data)


if __name__ == "__main__":
    db_client = pymongo.MongoClient("mongodb://localhost:27017")
    parser = GbBlogParser("https://gb.ru/posts", db_client, 0.5)
    parser.run()
