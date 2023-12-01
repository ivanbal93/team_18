from typing import Any

from scrapy import Spider
from scrapy.http import Response

from datetime import date


class KnifeSpider(Spider):
    name = "knife_spider"
    allowed_hosts = ["knife.media"]
    start_urls = ["https://knife.media/category/news/"]

    def info_from_page(self, response: Response):
        today = response.css('div.entry-header__info span.meta__item time::attr(datetime)').get()[:10]
        if today == str(date.today()):
            if response.css('h1.entry-header__title em::text').get():
                title = (response.css("h1.entry-header__title::text").get().replace('\xa0', ' ') +
                         response.css('h1.entry-header__title em::text').get().replace('\xa0', ' '))
            else:
                title = response.css("h1.entry-header__title::text").get().replace('\xa0', ' ')
            text = ' '.join(response.css("div.entry-content p::text").getall()).replace('\xa0', ' ')
            url = response.url
            category_list = response.css("div.entry-footer__tags a::text").getall()
            return {
                "title": title,
                "text": text,
                "url": url,
                "category_list": category_list,
                "site_id": 1
                }

    def parse(self, response: Response, **kwargs: Any) -> Any:
        links = response.css('div.widget-news__content a.widget-news__content-link::attr(href)').getall()
        for link in links:
            yield response.follow(url=link, callback=self.info_from_page)
