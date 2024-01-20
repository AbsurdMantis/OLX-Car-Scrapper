import json

urls = json.load(open('./urls.json', 'r'))

def del_null(urls):     
     rez = urls.copy()     
     for key, value in urls.items():     
        if value is 'null' or value == '':             
            del rez[key]         
        elif isinstance(value, dict):             
            rez[key] = del_null(value)     
            return rez
        
del_null(urls)