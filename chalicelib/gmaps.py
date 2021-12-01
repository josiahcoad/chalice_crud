import requests
import numpy as np

GMAP_KEY = 'AIzaSyCxfXAPgVM8ownCZdr8dFbQSg76chB7P4s'


def parse_place_details_result(result):
    return {
        'price_level': result.get('price_level', np.nan),
        'rating': result.get('rating', np.nan),
        'photos': [photo['photo_reference'] for photo in result.get('photos', [])],
        'formatted_address': result['formatted_address'],
        'lat': result['geometry']['location']['lat'],
        'lng': result['geometry']['location']['lng'],
        'gmap_url': result.get('url', ''),
    }


def query_place_details(url):
    res = requests.get(url)
    return parse_place_details_result(res.json()['result'])


def mk_place_details_url(place_id):
    url = f'https://maps.googleapis.com/maps/api/place/details/json?place_id={place_id}&key={GMAP_KEY}'
    return url


def get_place_details(place_id):
    url = mk_place_details_url(place_id)
    try:
        return query_place_details(url)
    except Exception as e:
        print(f'problem with "{place_id}":', e)
        return {}


def merge_place_details(place_id, place):
    return {**place, **get_place_details(place_id)}
