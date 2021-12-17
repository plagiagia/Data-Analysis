# IMPORTS
import config
import requests
import pandas as pd

COLS = ['name', 'wind.speed', 'clouds.all', 'main.temp',
        'main.pressure', 'main.humidity', 'main.temp_min', 'main.temp_max']


def get_weather_data(city):
    url = 'http://api.openweathermap.org/data/2.5/weather'
    params = {'q': city, 'appid': config.api_key, 'units': 'metric'}
    data = requests.get(url, params=params).json()
    df = pd.json_normalize(data)
    temp = df[COLS].copy()
    temp['description'] = pd.json_normalize(df['weather'][0][0])['description']
    return temp


if __name__ == '__main__':
    print(get_weather_data('Berlin'))
