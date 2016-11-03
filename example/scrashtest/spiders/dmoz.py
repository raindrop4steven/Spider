# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor

from scrapy_splash import SplashRequest


class DmozSpider(scrapy.Spider):
    name = "dmoz"
    allowed_domains = ["dmoz.org"]
    start_urls = ['http://www.dmoz.org/']

    # http_user = 'splash-user'
    # http_pass = 'splash-password'

    def parse(self, response):
        le = LinkExtractor()
        for link in le.extract_links(response):
            yield SplashRequest(
                link.url,
                self.parse_link,
                endpoint='render.json',
                args={
                    'har': 1,
                    'html': 1,
                }
            )

    def parse_link(self, response):
	yield {
	'title': response.css("title").extract(),
	'pages': response.data["har"]["log"]["pages"],
	'type': response.headers.get('Content-Type')
	}
