import requests
import pprint


def get_distance(address_origin, address_destination):
    parameters = {'origins': address_origin, 'destinations': address_destination,
                  'key': 'AIzaSyCkzqJoxe7QT6LeX6za_JWF0LDxfeAX2Ho'}
    base = 'https://maps.googleapis.com/maps/api/distancematrix/json'
    response = requests.get(base, parameters)
    answer = response.json()
    result = 0
    try:
        result = answer['rows'][0]['elements'][0]['distance']['value']
    except KeyError:
        result = 0
    return result
