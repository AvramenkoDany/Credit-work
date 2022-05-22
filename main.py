"""
                                Залікова робота
За посиланням https://registry.edbo.gov.ua/opendata/universities/
розміщено РЕЄСТР СУБ'ЄКТІВ ОСВІТНЬОЇ ДІЯЛЬНОСТІ (ЗАКЛАДИ ВИЩОЇ, ФАХОВОЇ ПЕРЕДВИЩОЇ ТА ПРОФЕСІЙНОЇ (ПРОФЕСІЙНО-ТЕХНІЧНОЇ) ОСВІТИ)
Завдання:
    1.Запитати у користувача код регіону
    2.Отримати ЗВО з вказаного користувачем регіону
    3.Зберегти всі дані у файл universities.csv у форматі csv
    4.Збережіть ті ж дані у файл universities_<код регіону>.csv, наприклад universities_80.csv
    5.Якщо регіон не зі списку доступних, то повідомити про це користувачеві у консолі
    6.Відфільтруйте і збережіть таку інформацію про заклади:
        Назви та ПІП керівників в файл rectors.csv
    7.Ускладніть програму з першого завдання наступним фільтром:
        З формою фінансування Державна
    8.Ускладніть програму з другого завдання можливістю фільтрування за будь-яким з наявних значень поля
"""


import requests
import csv

key = str(input('Введіть код регіону = '))

value0 = ['01', '05', '07']
value1 = [12, 14, 18, 21, 23, 26, 32, 35, 44, 46, 48, 51, 53, 56, 59, 61, 63, 65, 68, 71, 73, 74, 80, 85]

_check_0 = int(key) in value1
_check_1 = key in value0

if _check_0 is False:
    if _check_1 is False:
        print(f"This region isn't registered")
        exit(0)

print('Форма фінансування: ''Державна''/Приватна''/Комунальна')
choose = str(input("Обреріть щось одне з вибірки: "))

r = requests.get('https://registry.edbo.gov.ua/api/universities/?ut=1&lc=' + key + '&exp=json')
universities: list = r.json()

filteredData = [{k: row[k] for k in [
    'university_id',
    'university_parent_id',
    'close_date',
    'primitki',
    'university_edrpou',
    'university_governance_type_name',
    'university_financing_type_name',
]
                 } for row in universities]

filter_financing_type_name = [{k: row[k] for k in ['university_name',
                                                   'university_director_fio',
                                                   'university_financing_type_name'
                                                   ]
                               } for k in ['university_financing_type_name'] for row in universities if
                              row[k] == choose]

with open('universities.csv', mode='w', encoding='UTF-8') as _file:
    writer = csv.DictWriter(_file, fieldnames=filteredData[0].keys())
    writer.writeheader()
    writer.writerows(filteredData)

with open('universities_' + key + '.csv', mode='w', encoding='UTF-8') as _file:
    writer = csv.DictWriter(_file, fieldnames=filteredData[0].keys())
    writer.writeheader()
    writer.writerows(filteredData)

with open('rectors.csv', mode='w', encoding='UTF-8') as _file:
    writer = csv.DictWriter(_file, fieldnames=filter_financing_type_name[0].keys())
    writer.writeheader()
    writer.writerows(filter_financing_type_name)



