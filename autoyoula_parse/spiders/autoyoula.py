import scrapy
from Data_mining_2405.css_functions import make_dict
import pymongo


class AutoyoulaSpider(scrapy.Spider):
    name = 'autoyoula'
    allowed_domains = ['auto.youla.ru']
    start_urls = ['https://auto.youla.ru/']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.db_client = pymongo.MongoClient()

    def go_next(self, response, callback, css_link):
        for a_link in response.css(css_link):
            url = a_link.attrib['href']
            yield response.follow(url, callback=callback)

    def parse(self, response):
        yield from self.go_next(
            response,
            self.brand_parse,
            ".TransportMainFilters_brandsList__2tIkv a.blackLink")

    def brand_parse(self, response):

        sequence_tuple = (
            ("div.Paginator_block__2XAPy a.Paginator_button__u1e7D", self.brand_parse),
            ("article.SerpSnippet_snippet__3O1t2 a.SerpSnippet_name__3F7Yu", self.car_parse)
        )
        for css_link, callback in sequence_tuple:
            yield from self.go_next(
                response,
                callback,
                css_link)

    def car_parse(self, response):
        data = {
            "title": response.css(".AdvertCard_advertTitle__1S1Ak::text").extract_first(),
            "picture": [itm.attrib.get("src") for itm in response.css("figure.PhotoGallery_photo__36e_r img")],
            "price": response.css("div.AdvertCard_price__3dDCr::text").get().replace("\u2009", ""),
            "description": response.css(".AdvertCard_descriptionInner__KnuRi::text").extract_first(),
            "parameters": make_dict(
                            response,
                            "div.AdvertSpecs_label__2JHnS::text",
                            "div.AdvertSpecs_data__xK2Qx::text"),
            "equipment": make_dict(
                            response,
                            "div.AdvertEquipment_equipmentSection__3YpK5 div.h4::text",
                            "div.AdvertEquipment_equipmentItem__Jk5c4::text"),
        }
        self.db_client[self.crawler.settings.get("BOT_NAME", "parser")][self.name].insert_one(data)
