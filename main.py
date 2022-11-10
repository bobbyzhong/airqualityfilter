import network
import library as lib
import sys

def main() -> None:
    '''
    Main function to run the program
    '''
    type_loc, location = first_input()
    roa = second_input() 
    aqi_threshold = third_input()
    max_num = fourth_input()
    type_aqi, key_path = fifth_input()
    if type_aqi == 'PURPLEAIR':
        key_path = network.build_search_url(key_path)
    type_reverse, paths = sixth_input()
    center = network.ForwardGeocode(type_loc, location)
    center_point = center.get_coordinate()
    center_lat = float(center_point[0])
    center_lon = float(center_point[1])
    aqi_obj = network.Aqi(type_aqi, key_path)
    data = aqi_obj.get_aqi() 
    try:
        sorted_data = network.get_sorted_aqi(data, roa, max_num, aqi_threshold, center_lat, center_lon)
    except:
        print('FAILED')
        if type_aqi == 'PURPLEAIR':
            print(f'200 {aqi_obj.get_link()}')
        else: 
            print(aqi_obj.get_link())
        print('FORMAT')
        sys.exit(1)    
    print()  
    print(f'CENTER {center_lat}/N {center_lon}/W')
    i = 0
    for item in sorted_data:
        try:

            if type_reverse == 'NOMINATIM':
                reverse_geo = network.ReverseGeocode('NOMINATIM', None, item[2], item[3])
                description = reverse_geo.get_description()
            elif type_reverse == 'FILE':
                reverse_geo = network.ReverseGeocode('FILE', paths[i], item[2], item[3])
                description = reverse_geo.get_description()
                i += 1
        except:
            print('FAILED')
            if type_reverse == 'NOMINATIM':
                print(f'200 {reverse_geo.get_link()}')
            else: 
                print(reverse_geo.get_link())
            print('FORMAT')
            sys.exit(1)

        aqi = lib.convert_aqi(item[4])
        print(f'AQI {aqi}')
        print(f'{item[2]}/N {item[3]}/W')
        print(description)



def first_input() -> str:
    '''
    First line of input that takes the center location and the format
    the data is in
    '''
    text = input()
    text_list = text.split()
    location = ''
    if text_list[0] != 'CENTER':
        print('INVALID INPUT')
        sys.exit(1)
    if text_list[1] == 'NOMINATIM':
        type = 'NOMINATIM'
        for i in range(2, len(text_list)):
            location += text_list[i] + ' '
        return type, location.strip()

    elif text_list[1] == 'FILE':
        type = 'FILE'
        for i in range(2, len(text_list)):
            location += text_list[i] + ' '
        return type, location.strip()
    
def second_input() -> int:
    '''
    Takes the second line of input and returns the range of analysis
    '''
    text = input()
    if text.split()[0] != 'RANGE':
        print('INVALID INPUT')
        sys.exit(1)
    return int(text.split()[1])

def third_input() -> int:
    '''
    Takes the third line of input and returns an int representing the AQI threshold
    '''
    text = input()
    if text.split()[0] != 'THRESHOLD':
        print('INVALID INPUT')
        sys.exit(1)
    return int(text.split()[1])

def fourth_input() -> int:
    '''
    Takes the fourth line of input and returns an int representing the max number of locations
    we want to find in the search
    '''
    text = input()
    if text.split()[0] != 'MAX':
        print('INVALID INPUT')
        sys.exit(1)
    return int(text.split()[1])

def fifth_input() -> str:
    '''
    Takes the fifth line of input and returns the format the data is coming in and either 
    the API key or a path to where the data is
    '''
    text = input()
    text_list = text.split()
    if text_list[0] != 'AQI':
        print('INVALID INPUT')
        sys.exit(1)
    location = ''
    if text_list[1] == 'PURPLEAIR':
        return 'PURPLEAIR', text_list[2]
    elif text_list[1] == 'FILE':
        for i in range(2, len(text_list)):
            location += text_list[i] + ' '
        return 'FILE', location.strip()
def sixth_input() -> str:
    '''
    Takes the sixth line of input and returns the format the data is coming in and either 
    a string representing a file path to data or a list of strings representing
    file paths to data
    '''
    text = input()
    text_list = text.split()
    if text_list[0] != 'REVERSE':
        print('INVALID INPUT')
        sys.exit(1)
    file_list = []
    if text_list[1] == 'NOMINATIM':
        return 'NOMINATIM', None
    elif len(text_list) > 2:
        for i in range(2, len(text_list)):
            file_list.append(text_list[i])
        return 'FILE', file_list
    else:
        return 'FILE', text_list[2]

if __name__ == '__main__':
    main()

