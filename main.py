import requests
from pprint import pprint
import datetime
import os
# __________________________________________________________________________________
# Задача 1. Кто самый умный супергерой?

response = requests.get('https://akabab.github.io/superhero-api/api/' + '/all.json')

heroes = {
    'Hulk': 0,
    'Captain America': 0,
    'Thanos': 0
}

for hero in response.json():
    name = hero.get('name')
    if name in heroes:
        heroes[name] = hero.get('powerstats', {}).get('intelligence', 0)

heroes_sorted = list(sorted(heroes.items(), key=lambda x: x[1]))
print(heroes_sorted[-1])

# __________________________________________________________________________________
# Задача 2. Сохранение файла с компьютера на Яндекс.Диске с тем же названием (массовая загрузка файлов из заданной папки)

# Создаем функцию массовой загрузки в Яндекс Диск файлов из целевой папки
def file_upload_to_yandex_disk(file):
    file_link = directory + '\\' + file
    file_name = file_link.split('\\')

    # Указываем базовый URL для загрузки
    base_url = 'https://cloud-api.yandex.net'

    # Указываем токен для авторизации
    token = 'OAuth *здесь должен находиться код токена, выданный Яндекс Полигоном*'

    # Прописываем заголовки и URL для получения ссылки для загрузки файла в ЯД
    headers = {'Authorization': token}
    url_for_getting_link = base_url + '/v1/disk/resources/upload'

    # Указываем параметры (название загружаемого файла)
    params = {'path': file_name[-1]}

    # Создаем запрос для получения ссылки на загрузку файла, выполняем его, получаем ссылку
    response = requests.get(url_for_getting_link,
                            headers=headers,
                            params=params)
    url_upload = response.json().get('href', '')

    # Открываем на чтение бинарный файл 'rb', выполняем его передачу по полученной ссылке на ЯД как файл ({files='file: file})
    with open(file_link, "rb") as f:
        response = requests.put(url_upload, files={'file': f})

    # Проверяем статус выполнения передачи файла
    print(response.status_code)

# Получаем ссылку на целевую папку на компьютере, файлы которой будут загружены на ЯД
directory = input('Введите ссылку на папку для загрузки картинок в Яндекс.Диск: ')

# Обрабатываем введенную ссылку - получаем список файлов в ней, убираем лишние кавычки, если они есть во вводе
directory_list = directory.split(sep='\\')
if directory_list[-1][0] == '"':
    directory_list[-1] = directory_list[-1][:-1]
if directory_list[0][0] == '"':
    directory_list[0] = directory_list[0][1:]
directory = '\\'.join(directory_list)
files = os.listdir(directory)

# Для каждого файла из целевой папки выполняем функцию его передачи в Яндекс.Диск
for file in files:
    file_upload_to_yandex_disk(file)


# __________________________________________________________________________________
# Задача №3(необязательная). Написать программу, которая выводит все вопросы за последние два дня из Stackoverflow с тэгом Python

# Указываем базовый URL для подключения к серверу
base_url = 'https://api.stackexchange.com'

# Определяем две даты в формате UNIX (сколько секунд прошло с 01.01.1970 - из документации) - сегодня и два дня назад
previous_date = datetime.datetime.now() - datetime.timedelta(2)
seconds_since_epoch_two_days_ago = int(previous_date.timestamp())
seconds_since_epoch_now = int(datetime.datetime.now().timestamp())

# Указываем итоговый URL для получения информации по запросу в соответствии с условиями задачи (можно скачать на сайте Stackoverflow, заполнив вручную форму запроса)
url_for_getting_data = base_url + f'/2.3/questions?order=desc&min={seconds_since_epoch_two_days_ago}&max={seconds_since_epoch_now}&sort=creation&tagged="Python"&site=stackoverflow'

# Указываем, на каком именно ресурсе выполнить запрос (сайт Stackoverflow.com) - список можно посмотреть тут: https://api.stackexchange.com/2.2/sites
params = {'api_site_parameter': 'stackoverflow'}

# Формируем запрос с нужными параметрами
response = requests.get(url_for_getting_data, params=params)

# Получаем информация о статусе отработки запроса и ответ в виде файла json
print(response.status_code)
# pprint(response.json())

# Дополнительно (отсутствует в условиях задачи)- считаем количество вопросов в итоговом файле и выводим в pprint
counter = 0
response_list = (response.json().get('items'))
for i in response_list:
    counter += 1
print(f'За последние 2 дня на сайте Stackoverflow.com найдено {counter} вопросов с тегом "Python"')