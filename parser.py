import json
from bs4 import BeautifulSoup
from requests import get
url = 'https://tomi-ko.ru/catalog/323/'
url_home = 'https://tomi-ko.ru'
response_catalog = get(url)
bs4_1 = BeautifulSoup(response_catalog.content, 'html.parser')
pizza_dict = {}
for k in bs4_1.find_all('a'):
    if str(k.string)[:5] == 'Пицца':
        name_pizza = k.string
        pizza_dict[name_pizza] = {}
        url_page = url_home + k.attrs['href']
        response2 = get(url_page)
        bs4_2 = BeautifulSoup(response2.content, 'html.parser')
        price_text = bs4_2('div', 'catalog-element-price-discount')
        price = price_text[0].string.strip()
        pizza_dict[name_pizza]['price'] = price
        pizza_description = bs4_2.find('div',  class_=['catalog-element-description', 'catalog-element-description-preview', 'intec-ui-markup-text'])
        pizza_dict[name_pizza]['description'] = str(pizza_description.contents[0]).replace('.', '').strip()
        if 'Пицца Маргарита' in k.string:
            pizza_dict[name_pizza]['description'] = str(pizza_description.contents[0]).replace('Моцерелла', 'Моцарелла').replace('.', '').strip()
        pizza_dict[name_pizza]['url'] = url_page
json_data = json.dumps(pizza_dict, ensure_ascii=False, indent=4)
with open('pizzas.json', 'w', encoding='utf-8') as json_file:
    json_file.write(json_data)
