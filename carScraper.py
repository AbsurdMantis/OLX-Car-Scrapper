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
        urls = json.load(open('./urls.json', 'r'))
        headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:48.0) Gecko/20100101 Firefox/48.0'}
        for link in urls:
            yield scrapy.Request(link['url'], headers=headers)
        

 
    def parse(self, response, **kwargs):
        script_data = response.css('script#initial-data::attr(data-json)').get()
        cleaned_content = script_data.replace('\r', '').replace('\n', '').replace('\t', '')

        data_json = json.loads(cleaned_content)

        ad = data_json['ad']

        properties = ad['properties']

        opcionais = [prop['value'] for prop in properties if prop['name'] == 'car_features'][0]

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
            
        cartype_mapping = {'Antigo': 0, 'Buggy': 1, 'Caminhão Leve': 2, 'Conversível': 3, 'Hatch': 4, 'Passeio': 5, 'Pick-up': 6, 'Sedã': 7, 'SUV': 8, 'Van/Utilitário': 9}
        motorpower_mapping = {'1.0': 0, '1.2': 1, '1.3': 2, '1.4': 3, '1.5': 4, '1.6': 5, '1.7': 6, '1.8': 7, '1.9': 8, '2.0 - 2.9': 9, '3.0 - 3.9': 10, '4.0 ou mais': 11}
        fuel_mapping = {'Gasolina': 0, 'Álcool': 1, 'Flex': 2, 'Diesel': 3, 'Híbrido': 4, 'Elétrico': 5, 'Gás Natural': 6}
        gnv_mapping = {'Não': 0, 'Sim': 1}
        gearbox_mapping = {'Manual': 0, 'Automático': 1, 'Semi-Automático': 2, 'Semi-automático': 2}
        color_mapping = {'Preto': 0, 'Branco': 1, 'Prata': 2, 'Vermelho': 3, 'Cinza': 4, 'Azul': 5, 'Amarelo': 6, 'Verde': 7, 'Laranja': 8, 'Outra': 9}
        doors_mapping = {'2 portas': 0, '4 portas': 2}
        steering_mapping = {'Hidráulica': 0, 'Elétrica': 1, 'Mecânica': 2, 'Assistida': 3}

        newline = {
            'url': ad['friendlyUrl'],
            'title' : ad['subject'],
            'price' : ad['price'],
            'description' : ad['body'],
            'model' : [prop['value'] for prop in properties if prop['name'] == 'vehicle_model'][0],
            'brand' : [prop['value'] for prop in properties if prop['name'] == 'vehicle_brand'][0],
            'cartype': cartype_mapping.get([prop['value'] for prop in properties if prop['name'] == 'cartype'][0], -1),
            'regdate': [prop['value'] for prop in properties if prop['name'] == 'regdate'][0],
            'mileage': [prop['value'] for prop in properties if prop['name'] == 'mileage'][0],
            'motorpower': motorpower_mapping.get(next((prop['value'] for prop in properties if prop['name'] == 'motorpower'), None), -1),
            'fuel': fuel_mapping.get(next((prop['value'] for prop in properties if prop['name'] == 'fuel'), None), -1),
            'gnv_kit': gnv_mapping.get(next((prop['value'] for prop in properties if prop['name'] == 'gnv_kit'), None), -1),
            'gearbox': gearbox_mapping.get(next((prop['value'] for prop in properties if prop['name'] == 'gearbox'), None), -1),
            'carcolor': color_mapping.get(next((prop['value'] for prop in properties if prop['name'] == 'carcolor'), None), -1),
            'doors': doors_mapping.get(next((prop['value'] for prop in properties if prop['name'] == 'doors'), None), -1),
            'car_steering': steering_mapping.get(next((prop['value'] for prop in properties if prop['name'] == 'car_steering'), None), -1)
        }

        newline.update(opcionais_variables)

        yield newline


