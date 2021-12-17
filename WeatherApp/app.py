import database
import api_call

def run(city):
    weather_data = api_call.get_weather_data(f'{city}')
    # Fill database with weather data
    database.insert_data(*[each for each in weather_data.values[0]])


