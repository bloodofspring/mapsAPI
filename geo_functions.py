import math

import requests


def geocode(toponym_to_find):
    geocoder_api_server = "http://geocode-maps.yandex.ru/1.x/"
    geocoder_params = {
        "apikey": "8013b162-6b42-4997-9691-77b7074026e0",
        "geocode": toponym_to_find,
        "format": "json"}
    response = requests.get(geocoder_api_server, params=geocoder_params)
    if not response:
        # обработка ошибочной ситуации
        pass
    # Преобразуем ответ в json-объект
    json_response = response.json()
    # Получаем первый топоним из ответа геокодера.
    toponym = json_response["response"]["GeoObjectCollection"][
        "featureMember"][0]["GeoObject"]
    return toponym if toponym else None


def get_coordinates(toponym_to_find):
    toponym = geocode(toponym_to_find)
    if not toponym:
        return None, None
    toponym_coordinates = toponym['Point']['pos']
    toponym_longitude, toponym_lattitude = toponym_coordinates.split(' ')
    toponym_longitude = float(toponym_longitude)
    toponym_lattitude = float(toponym_lattitude)
    return toponym_longitude, toponym_lattitude


def get_ll_span(toponym_to_find):
    toponym = geocode(toponym_to_find)
    if not toponym:
        return None, None
    toponym_coordinates = toponym['Point']['pos']
    toponym_longitude, toponym_lattitude = toponym_coordinates.split(' ')

    ll = ','.join([toponym_longitude, toponym_lattitude])
    left, bottom = toponym['boundedBy']['Envelope']['lowerCorner'].split(' ')
    right, top = toponym['boundedBy']['Envelope']['upperCorner'].split(' ')

    dx = abs(float(left) - float(right)) / 2
    dy = abs(float(top) - float(bottom)) / 2
    span = f'{dx},{dy}'
    return ll, span


def find_business(text, ll, spn, lang='ru_RU'):
    search_api_server = "https://search-maps.yandex.ru/v1/"
    api_key = "dda3ddba-c9ea-4ead-9010-f43fbc15c6e3"
    search_params = {
        'apikey': api_key,
        'text': text,
        'lang': lang,
        'll': ll,
        'spn': spn,
        'type': 'biz'
    }
    response = requests.get(search_api_server, params=search_params)
    if not response:
        pass
    json_response = response.json()
    return json_response['features'][0]


def lonlat_distance(a, b):
    degree_to_meters_factor = 111_000
    a_lon, a_lat = a
    b_lon, b_lat = b

    radians_lattitude = math.radians((a_lat + b_lat) / 2)
    lat_lon_factor = math.cos(radians_lattitude)

    dx = abs(a_lon - b_lon) * degree_to_meters_factor * lat_lon_factor
    dy = abs(a_lat - b_lat) * degree_to_meters_factor

    distance = math.sqrt(dx ** 2 + dy ** 2)

    return distance
