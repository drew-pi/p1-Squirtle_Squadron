import requests

'''
Returns the key in the specified file in string format
'''
def get_key(file_n:'file name as str'):
    path = f'keys/{file_n}'

    with open(path) as key:
        return key.read().strip('\n')


'''
Uses api ninjas city api to get population of a given city in a given country
'''
def city_pop(n:'name',c:'country'):

    # docs: https://api-ninjas.com/api/city

    file_name = 'key_citypop.txt'
    api_url = "https://api.api-ninjas.com/v1/city?"
    params = {
        'name':{n},
        'country':{c}
    }
    response = requests.get(api_url, params=params, headers={'X-Api-Key': get_key(file_name)})
    # making sure that the api requests came back properly
    if response.status_code == requests.codes.ok:
        return(response.text)
    else:
        print("Error:", response.status_code, response.text)


'''
stored in database like this: "<city_name>:[<lat>,<lon>]" in string form so that we can parse
'''
def city_weather(entry: "found in a sqlite table in the above format"):

    # docs: https://openweathermap.org/current

    file_name = "key_cityweather.txt"
    api_url = "https://api.openweathermap.org/data/2.5/weather?"

    # parsing of entry
    city = entry[:entry.find(":")]
    coords = entry[entry.find("[")+1:entry.find("]")]
    lat = float(coords[:coords.find(",")])
    lon = float(coords[coords.find(",")+1:])

    # params = {
    #     "lat":lat,
    #     "lon":lon,
    #     'units':'imperial',
    #     "appid":get_key(file_name)
    # }
    # response = requests.get(api_url, params =params) # doesn't work for some reason

    url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&units=imperial&appid={get_key(file_name)}"
    response = requests.get(url)

    # making sure that the api requests came back properly
    if response.status_code != requests.codes.ok:
        print("Error:", response.status_code, response.text)
        return

    # parsing the json return
    





print(city_pop('Birmingham', 'GB'))
print(city_weather("New York:[40.73, -73.93]"))