from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings

from autoyoula_parse.spiders.autoyoula import AutoyoulaSpider


if __name__ == "__main__":
    crawler_settings = Settings()
    crawler_settings.setmodule("autoyoula_parse.settings")
    crawler_process = CrawlerProcess(settings=crawler_settings)
    crawler_process.crawl(AutoyoulaSpider)
    crawler_process.start()