from openpyxl import load_workbook
import json
file_name = 'example.xlsx'
wb = load_workbook(file_name)
ws = wb['Лист1']
cols = ['Название пиццы', 'Состав', 'Цена', 'Ссылка на товар']
ws.append(cols)
wb.save(file_name)
def filter(prev_dict, necessary=None, exceptions=None):
    total_dict = {}
    for key, value in prev_dict.items():
        ingredients = set(prev_dict[key]['description'].replace('.', '').lower().split(', '))
        if necessary is None:
            if len(ingredients.intersection(exceptions)) == 0:
                total_dict[key] = value
        elif exceptions is None:
            if len(ingredients.intersection(necessary)) > 0:
                total_dict[key] = value
    return total_dict


with open('pizzas.json', 'r', encoding='utf-8') as json_file:
    pizza_dict = json.load(json_file)
pork = {'ветчина', 'пепперони', 'свинина', 'салями', 'бекон', 'охотничыи колбаски', 'сервелат', ' 1-4 неополитанская',
        '1-4 техасская'}
cheese = {'моцарелла', 'сулугуни', 'чеддер', 'гауда', 'дорблю', 'сыр пармезан', 'фета', 'дор блю', 'пармезан',
          'моцарелла в рассоле', 'сливочный сыр'}
res = pizza_dict.copy()
choice = input('Пицца должна быть без свинины?(Y/N) ')
if choice == 'Y':
    res = filter(res, exceptions=pork)
choice = input(
    'С каким из этих сыров вы хотите пиццу, пропишите названия через пробел(моцарелла, сулугуни, чеддер, гауда, дорблю, сыр пармезан)? ')
if len(choice) > 0:
    res = filter(res, necessary=set(choice.split()))
for key, value in res.items():
    ws.append([key, value['description'], value['price'], value['url']])
    wb.save(file_name)
print(res)
