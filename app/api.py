from pprint import pprint
import requests
import random

def get_cities():
    # Choose two random cities from the API response
    api_key = 'f9ca0722a830a37dcd77c39571e64d6f691cdefe'
    api_url = f'https://api.census.gov/data/2019/pep/population?get=NAME,POP&for=place:*&in=state:*&key={api_key}'
    api_response = requests.get(api_url).json()
    cities = random.sample(api_response[1:], 2)

    # Save the names and populations of the two cities as global variables
    global city1, city2, city1_pop, city2_pop
    city1 = cities[0][0]
    city2 = cities[1][0]
    city1_pop = int(cities[0][1])
    city2_pop = int(cities[1][1])

'''
Returns the key in the specified file in string format
'''
def get_key(file_name: str):
    path = f'keys/{file_name}'

    with open(path) as key:
        return key.read().strip('\n')


'''
Uses api ninjas city api to get population of a given city in a given country
'''
def city_pop(name,country):

    # docs: https://api-ninjas.com/api/city

    file_name = 'key_citypop.txt'
    api_url = "https://api.api-ninjas.com/v1/city?"
    params = {
        'name':{name},
        'country':{country}
    }
    response = requests.get(api_url, params=params, headers={'X-Api-Key': get_key(file_name)})
    # making sure that the api requests came back properly
    if response.status_code == requests.codes.ok:
        print(response.json())
        return(response.json())
    else:
        print("Error:", response.status_code, response.text)


'''
stored in database like this: "<city_name>:[<lat>,<lon>]" in string form so that we can parse
found in a sqlite table in the above format
'''
def city_weather(entry):

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
    return response.json()
    
def get_city_img(name): 

    api_url = "https://api.pexels.com/v1/search?"
    file_name = "key_cityimg.txt"

    params = {
        "query":{name},
        "per_page":{1}
    }

    response = requests.get(api_url,params=params,headers={"Authorization":get_key(file_name)})

    # parsing the response
    data = response.json()
    img_url = data['photos'][0]['src']['original']
    site_url = data['photos'][0]['url']
    print("this is the site picture: " + site_url)
    return img_url



def get_rand_city():

    # documentation: http://geodb-cities-api.wirefreethought.com/demo

    api_url = "http://geodb-free-service.wirefreethought.com/v1/geo/cities?"

    params = {
        "minPopulation":1000000,
        "limit":1,
        "offset":random.randint(0,1530)
    }

    response = requests.get(api_url,params=params)
    
    # parsing of response
    data = response.json()
    print(response.json())
    city_name = data['data'][0]['city']
    country = data['data'][0]['country']
    region = data['data'][0]['region']
    latitude = data['data'][0]['latitude']
    longitude = data['data'][0]['longitude']
    # print({'city':city_name,'country':country,"region":region})

    return {'city':city_name,'country':country,"region":region, "latitude":latitude, "longitude":longitude}




# get_city_img("Lexinton")
resp = get_rand_city()
print("city of " + resp['city'] + " " + resp['region'] + " " + resp['country'])
print (get_city_img("city of " + resp['city'] + " " + resp['country']))
print(city_weather(resp['city']+":["+str(resp['latitude'])+","+str(resp['longitude'])+"]"))


