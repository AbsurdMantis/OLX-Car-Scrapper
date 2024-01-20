import json

with open('../data/urls.json') as json_file:
    url_data = json.load(json_file)

filter_words = ['repasse', 'sucata','batido','retirada','peças','quebrado']

non_null_entries = [entry for entry in url_data if entry['url'] != 'null' and all(word not in entry['url'] for word in filter_words)]

save_json = json.dumps(non_null_entries)

with open('../data/filteredURL.json', 'w') as outfile:
    outfile.write(save_json)