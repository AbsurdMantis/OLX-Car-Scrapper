import scrapy
import json

class CarPageOLX(scrapy.Spider):
    name = 'olx'
 
    custom_settings = {
        'USER_AGENT' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36',
        'AUTOTHROTTLE_ENABLED': True,
        'AUTOTHROTTLE_START_DELAY': 10
        
    }

    def start_requests(self):
        urls = json.load(open('./urls.json', 'r'))
        headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:48.0) Gecko/20100101 Firefox/48.0'}
        for link in urls:
            yield scrapy.Request(link, headers=headers)
 
    def parse(self, response, **kwargs):
        html = json.loads(response.xpath('//script[@id="__NEXT_DATA__"]/text()').get())
        links = html.get('props').get('pageProps').get('ads')
        for link in links:
            yield{
                'url' : link.get('url'),
            }


