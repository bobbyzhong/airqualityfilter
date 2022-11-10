import json
import library as lib
import urllib.parse as parse
import urllib.request
import sys

# AQI_KEY = '87255AF7-593D-11ED-B5AA-42010A800006'

class Aqi:
    def __init__(self, data_location: str, pathlink: str):
        '''
        Initializes an AQI object with a link and the data it contains
        '''
        if data_location == 'FILE':
            self.link = pathlink
            try:
                with open(pathlink) as f:
                    self.data = json.load(f)
            except:
                print('FAILED')
                print(pathlink)
                print('MISSING')
                sys.exit(1)
        elif data_location == 'PURPLEAIR':
            response = None
            try:
                self.data = lib.open_read_link(pathlink)
                self.link = pathlink
            except urllib.error.HTTPError as e: 
                print('FAILED')
                print(f'{e.code} {pathlink}')
                if e.code != 200:
                    print('NOT 200')
                sys.exit(1)

    def get_aqi(self) -> tuple:
        ''' Returns the data about the aqi'''
        return self.data
    def get_link(self) -> str:
        ''' Returns the link to where the data was received from '''
        return self.link

class ForwardGeocode:
    def __init__(self, type: str, place_filepath: 'str'):
        ''' Initializes forward geocode object with the coorindates '''
        if type == 'FILE':
            data = lib.read_file(place_filepath)
            try:
                self.coordinate = data[0]['lat'], data[0]['lon']
            except:
                print('FAILED')
                print(place_filepath)
                print('FORMAT')
                sys.exit(1)
        elif type == 'NOMINATIM':
            try: 
                url = 'https://nominatim.openstreetmap.org/search?'
                query_parameters = [
                    ('header', 'bobbyz2'), ('format', 'json'), ('q', place_filepath)
                ]
                encoded = parse.urlencode(query_parameters)
                url += encoded
                data = lib.open_read_link(url)
                self.coordinate = data[0]['lat'], data[0]['lon']
            except urllib.error.HTTPError as e: 
                print('FAILED')
                print(f'{e.code} {url}')
                if e.code != 200:
                    print('NOT 200')
                sys.exit(1)

    def get_coordinate(self) -> tuple:
        ''' Returns a tuple representing coordinates of the center '''
        return self.coordinate  

class ReverseGeocode:
    def __init__(self, type: str, file: 'str', lat: 'float', lon: 'float'):
        ''' 
        Initializes Reverse Geocode object with the decription of location 
        a link to where the information was retreived from
        '''
        if type == 'FILE':
            data = lib.read_file(file)
            self.description = data['display_name']
            self.link = file
            
        elif type == 'NOMINATIM':
            try: 
                url = 'https://nominatim.openstreetmap.org/reverse?'
                query_parameters = [
                    ('format', 'json'), ('lat', lat), ('accept-language', 'en-US'), ('lon', lon)
                ]
                encoded = parse.urlencode(query_parameters)
                url += encoded
                data = lib.open_read_link(url)
                self.description =  data['display_name']
                self.link = url
            except urllib.error.HTTPError as e: 
                print('FAILED')
                print(f'{e.code} {url}')
                if e.code != 200:
                    print('NOT 200')
                sys.exit(1)

    def get_description(self) -> str:
        ''' Returns the description of the location '''
        return self.description
    def get_link(self) -> str:
        ''' Returns the link from which the data was retrieved from '''
        return self.link

def get_sorted_aqi(data: object, dist: int, max: int, aqi_thresh: int, center_lat: float, center_lon: float) -> list[list]:
    '''
    Takes the data and parameters such as aqi threshold and returns a list containing only 
    locations that fit all the requirements
    '''
    sorted_list = []
    count = 0
    for i in range(len(data['data'])):
        if data['data'][i][2] == None or data['data'][i][3] == None:
            continue
        if data['data'][i][4] == None:
            continue
        lat = float(data['data'][i][2])
        lon = float(data['data'][i][3])
        distance = abs(lib.determine_distance(center_lat, center_lon, lat, lon))
        pm = float(data['data'][i][4])
        aqi = lib.convert_aqi(pm)
        if aqi >= aqi_thresh:
            if distance <= dist:
                sorted_list.append(data['data'][i])
                count += 1
        if count == max:
            break
    return sorted_list

def build_search_url(key: str):
    query_parameters = [
        ('api_key', key), ('fields', ('sensor_index,name,longitude,latitude,pm2.5')), ('location_type', 0), ('max_age', 3600)
    ]
    encoded = parse.urlencode(query_parameters)
    return f'https://api.purpleair.com/v1/sensors?' + encoded
