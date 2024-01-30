import scrapy
import json

class CarPageOLX(scrapy.Spider):
    name = 'olx_carscraper'
 
    custom_settings = {
        'USER_AGENT' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36',
        'AUTOTHROTTLE_ENABLED': True,
        'AUTOTHROTTLE_START_DELAY': 10
        
    }

    def start_requests(self):
        urls = json.load(open('./data/filteredURL.json', 'r'))
        headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:48.0) Gecko/20100101 Firefox/48.0'}
        for link in urls:
            yield scrapy.Request(link['url'], headers=headers)
        

 
    def parse(self, response, **kwargs):
        script_data = response.css('script#initial-data::attr(data-json)').get()
        cleaned_content = script_data.replace('\r', '').replace('\n', '').replace('\t', '')

        data_json = json.loads(cleaned_content)

        ad = data_json['ad']

        properties = ad['properties']

        try:
            opcionais = [prop['value'] for prop in properties if prop['name'] == 'car_features'][0]
        except:
            opcionais = ''

        opcionais_mapping = {
            'Air bag': 'airbag',
            'Alarme': 'alarme',
            'Ar condicionado': 'ar_condicionado',
            'Trava elétrica': 'trava_eletrica',
            'Vidro elétrico': 'vidro_eletrico',
            'Som': 'som',
            'Sensor de ré': 'sensor_re',
            'Câmera de ré': 'camera_re',
            'Blindado': 'blindado',
        }

        opcionais_variables = {feature: 0 for feature in opcionais_mapping.values()}
        for i in opcionais.split(','):
            if i.strip() in opcionais_mapping:
                opcionais_variables[opcionais_mapping[i.strip()]] = 1
            
        cartype_mapping = {'Antigo': 1, 'Buggy': 2, 'Caminhão Leve': 3, 'Conversível': 4, 'Hatch': 5, 'Passeio': 6, 'Pick-up': 7, 'Sedã': 8, 'SUV': 9, 'Van/Utilitário': 10}
        motorpower_mapping = {'1.0': 1, '1.2': 2, '1.3': 3, '1.4': 4, '1.5': 5, '1.6': 6, '1.7': 7, '1.8': 8, '1.9': 9, '2.0 - 2.9': 10, '3.0 - 3.9': 11, '4.0 ou mais': 12}
        fuel_mapping = {'Gasolina': 1, 'Álcool': 2, 'Flex': 3, 'Diesel': 4, 'Híbrido': 5, 'Elétrico': 6, 'Gás Natural': 7}
        gnv_mapping = {'Não': 1, 'Sim': 2}
        gearbox_mapping = {'Manual': 1, 'Automático': 2, 'Semi-Automático': 3, 'Semi-automático': 4}
        color_mapping = {'Preto': 1, 'Branco': 2, 'Prata': 3, 'Vermelho': 4, 'Cinza': 5, 'Azul': 6, 'Amarelo': 7, 'Verde': 8, 'Laranja': 9, 'Outra': 10}
        doors_mapping = {'2 portas': 1, '4 portas': 2}
        steering_mapping = {'Hidráulica': 1, 'Elétrica': 2, 'Mecânica': 3, 'Assistida': 4}

        newline = {
            'url': ad['friendlyUrl'],
            'title' : ad['subject'],
            'price' : ad['price'],
            'description' : ad['body'],
            'model' : [prop['value'] for prop in properties if prop['name'] == 'vehicle_model'][0],
            'brand' : [prop['value'] for prop in properties if prop['name'] == 'vehicle_brand'][0],
            'cartype': cartype_mapping.get(next((prop['value'] for prop in properties if prop['name'] == 'cartype'), None), 0),
            'regdate': [prop['value'] for prop in properties if prop['name'] == 'regdate'][0],
            'mileage': [prop['value'] for prop in properties if prop['name'] == 'mileage'][0],
            'motorpower': motorpower_mapping.get(next((prop['value'] for prop in properties if prop['name'] == 'motorpower'), None), 0),
            'fuel': fuel_mapping.get(next((prop['value'] for prop in properties if prop['name'] == 'fuel'), None), 0),
            'gnv_kit': gnv_mapping.get(next((prop['value'] for prop in properties if prop['name'] == 'gnv_kit'), None), 0),
            'gearbox': gearbox_mapping.get(next((prop['value'] for prop in properties if prop['name'] == 'gearbox'), None), 0),
            'carcolor': color_mapping.get(next((prop['value'] for prop in properties if prop['name'] == 'carcolor'), None), 0),
            'doors': doors_mapping.get(next((prop['value'] for prop in properties if prop['name'] == 'doors'), None), 0),
            'car_steering': steering_mapping.get(next((prop['value'] for prop in properties if prop['name'] == 'car_steering'), None), 0)
        }

        newline.update(opcionais_variables)

        yield newline


