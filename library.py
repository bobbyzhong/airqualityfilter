import json
import math
from decimal import Decimal, ROUND_HALF_UP
import sys
import urllib.parse as parse
import urllib.request

def determine_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    '''
    Determines the distance between two points
    '''
    dlat = (math.pi/180)*(lat2 - lat1)
    dlon = (math.pi/180)*(lon2 - lon1)
    alat = (math.pi/180)*((lat1 + lat2)/2)
    R = 3958.8
    x = dlon * math.cos(alat)
    d = math.sqrt(x*x + dlat*dlat) * R
    return d

def read_file(path) -> dict:
    '''
    Takes a path to a file containing json data and returns 
    data in the form of python dictionary
    '''
    try:
        with open(path) as f:
            data = json.load(f)
        return data
    except:
        print('FAILED')
        print(path)
        print('MISSING')
        sys.exit(1)
    finally:
        f.close()

def open_read_link(link: str) -> dict:
    '''
    Takes a URL and returns a python dictionary representing the parsed JSON response
    '''
    request = urllib.request.Request(link, method='GET')
    response = urllib.request.urlopen(request) 
    json_text = response.read().decode(encoding = 'utf-8')
    
    data = json.loads(json_text)
    if response != None:
        response.close()
    return data

def convert_aqi(pm: float) -> int:
    '''
    Calculates and returns an AQI value given a PM2.5 Concentration
    '''

    if 0.0 <= pm < 12.1:
        slope = 50/12
        aqi = Decimal(slope * pm).quantize(0, ROUND_HALF_UP)
        return aqi
    elif 12.1 <= pm < 35.5:
        slope = 49/23.3
        aqi = Decimal(51 + (slope * (pm - 12.1))).quantize(0, ROUND_HALF_UP)
        return aqi
    elif 35.5 <= pm < 55.5:
        slope = 49/19.9
        aqi = Decimal(101 + (slope * (pm - 35.5))).quantize(0, ROUND_HALF_UP)
        return aqi
    elif 55.5 <= pm < 150.5:
        slope = 49/94.9
        aqi = Decimal(151 + (slope * (pm - 55.5))).quantize(0, ROUND_HALF_UP)
        return aqi
    elif 150.5 <= pm < 250.5:
        slope = 99/99.9
        # aqi = round(201 + (slope * (pm - 150.5)))
        aqi = Decimal(201 + (slope * (pm - 150.5))).quantize(0, ROUND_HALF_UP)
        return aqi
    elif 250.5 <= pm < 350.5:
        slope = 99/99.9
        # aqi = round(201 + (slope * (pm - 150.5)))
        aqi = Decimal(301 + (slope * (pm - 250.5))).quantize(0, ROUND_HALF_UP)
        return aqi
    elif 350.5 <= pm < 500.5:
        slope = 99/149.9
        # aqi = round(201 + (slope * (pm - 150.5)))
        aqi = Decimal(401 + (slope * (pm - 350.5))).quantize(0, ROUND_HALF_UP)
        return aqi
    elif pm >= 500.5:
        return 501

def delete_replace(data: object, file: str) -> None:
    with open(file, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)