import requests
import json
import datetime as dt
# ciudades
# -san pedro
# -la plata
# -escobar


moreno_lat, moreno_long = (-34.6506, -58.7897)

escobar_lat, escobar_long = (-34.34833, -58.79265)

laPlata_lat, laPlata_long = (-34.92145, -57.95453)

sanPedro_lat, sanPedro_long = (-33.67918, -59.66633)


def get_data(lat, long, city):

    url = f'https://archive-api.open-meteo.com/v1/archive?latitude={lat}&longitude={long}&start_date=2020-01-01&end_date=2022-12-31&hourly=relativehumidity_2m&daily=temperature_2m_max,temperature_2m_min,temperature_2m_mean,precipitation_sum&timezone=America%2FSao_Paulo'
    city_data = requests.get(url).json()
    json_data = json.dumps(city_data)
    with open(f'{city}.json', 'w') as f:
        f.write(json_data)

city = 'laplata'
long = laPlata_long
lat = laPlata_lat
get_data(lat, long,city)


humidity_lst = {}


def structure_data(city):
    f = open(f'{city}.json')
    data = json.load(f)
    hourly = data['hourly']
    current_date = False
    for index, hour in enumerate(hourly['time']):
        date = hour.split('T')[0].split('-')
        date = date[0] + '-' + date[1]
        humidity = hourly['relativehumidity_2m'][index]
        if (date != current_date):
            humidity_lst[date] = []
        humidity_lst[date].append(humidity)
        current_date = date


humidity_averages = {}


def humidity_hourly_to_daily(humidity_lst):
    for month in humidity_lst:
        average = average_func(humidity_lst[month])
        humidity_averages[month] = average


def average_func(lst):
    return sum(lst)/len(lst)

# data 1 =
structure_data(city)
humidity_hourly_to_daily(humidity_lst)
# resuelve en : (humidity_averages)


def average_daylis(city):
    f = open(f'{city}.json')
    data = json.load(f)
    daily = data['daily']
    structured_data = {}
    current_date = False

    for index, date in enumerate(daily['time']):
        maxT = daily['temperature_2m_max'][index]
        minT = daily['temperature_2m_min'][index]
        avgT = daily['temperature_2m_mean'][index]
        prec = daily['precipitation_sum'][index]
        date = date.split('-')
        date = date[0] + '-' + date[1]
        if (date != current_date):
            structured_data[date] = {'max': [], 'min': [], 'avg': [], 'prec': []}
        structured_data[date]['max'].append(maxT)
        structured_data[date]['min'].append(minT)
        structured_data[date]['avg'].append(avgT)
        structured_data[date]['prec'].append(prec)
        
        current_date = date
        # print({'max': maxT,'min':minT,'avg':avgT,'prec':prec})
    test = {}
    for key in structured_data:
        test[key] = {}
        test[key]['hum'] = humidity_averages[key]
        for list in structured_data[key]:
            test[key][list] =  average_func(structured_data[key][list])
            

    return test


data_final = (average_daylis(city))

with open(f'{city}_final.json', 'w') as f:
        data_final = json.dumps(data_final)
        f.write(data_final)