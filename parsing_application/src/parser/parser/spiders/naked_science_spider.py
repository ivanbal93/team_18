from datetime import date
from typing import Any

from scrapy import Spider
from scrapy.http import Response


class NakedScienceSpider(Spider):
    name = "naked_science_spider"
    allowed_hosts = ["naked-science.ru"]
    start_urls = ["https://naked-science.ru/article"]

    def info_from_page(self, response: Response):
        today = response.css('div.title span.echo_date::attr(data-published)').get()[:10]
        if today == str(date.today()):
            title = response.css('div.post-title h1::text').get()
            text = ' '.join(response.css('div.body p::text').getall())
            url = response.url
            category_list = []
            for cat in response.css('div.terms-wrapp a.animate-custom::text').getall():
                if not cat.startswith('\n'):
                    category_list.append(cat.replace('# ', ''))
            views = int(response.css('div.fvc-view span.fvc-count::text').get())
            return {
                "title": title,
                "text": text,
                "url": url,
                "category_list": category_list,
                "site_id": 2,
                "views": views,
                "like": 0,
                "repost": 0
                }

    def parse(self, response: Response, **kwargs: Any) -> Any:
        links = response.css('div.news-item-title a.animate-custom::attr(href)').getall()
        for link in links:
            yield response.follow(url=link, callback=self.info_from_page)
