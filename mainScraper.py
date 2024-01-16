import scrapy
import json
 
class OlxCars(scrapy.Spider):
    name = 'olx'
 
    custom_settings = {
        'USER_AGENT' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36',
        'AUTOTHROTTLE_ENABLED': True,
        'AUTOTHROTTLE_START_DELAY': 10
        
    }

    
 
    def start_requests(self):
        ufs = ['sp', 'ac', 'al', 'ap', 'am', 'ba', 'ce', 'df', 'es', 'go', 'ma', 'mt', 'ms', 'mg', 'pa', 'pb', 'pr', 'pe', 'pi',
       'rj', 'rn', 'rs', 'ro', 'rr', 'sc', 'sp', 'se', 'to']
        headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:48.0) Gecko/20100101 Firefox/48.0'}
        length = 1000
        for uf in ufs:
            for price in range(5000, 300001, length):   
                for page in range(1, 101):
                    if price >= 150000:
                        if page == 1:
                            url = 'https://www.olx.com.br/autos-e-pecas/carros-vans-e-utilitarios/estado-{}?ps={}'.format(uf,price)
                        else:
                            url = 'https://www.olx.com.br/autos-e-pecas/carros-vans-e-utilitarios/estado-{}?ps={}&o={}'.format(uf,price,page)
                    else:
                        if page == 1:
                            url = 'https://www.olx.com.br/autos-e-pecas/carros-vans-e-utilitarios/estado-{}?pe={}&ps={}'.format(uf,price, price-length)
                        else:
                            url = 'https://www.olx.com.br/autos-e-pecas/carros-vans-e-utilitarios/estado-{}?pe={}&ps={}&o={}'.format(uf,price, price-length,page)
                    yield scrapy.Request(url, headers=headers)
 
    def parse(self, response, **kwargs):
        html = json.loads(response.xpath('//script[@id="_NEXT_DATA_"]/text()').get())
        links = html.get('props').get('pageProps').get('ads')
        for link in links:
            yield{
                'url' : link.get('url'),
            }