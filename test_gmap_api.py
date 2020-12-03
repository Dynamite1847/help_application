import requests
import pprint


address='6952 av de monts'
parameters = {'address': address, 'key': 'AIzaSyCkzqJoxe7QT6LeX6za_JWF0LDxfeAX2Ho'}
base = 'https://maps.googleapis.com/maps/api/geocode/json'
response = requests.get(base, parameters)
answer = response.json()
pprint.pprint(answer)
print(answer['results'][0]['geometry']['location']['lat'])