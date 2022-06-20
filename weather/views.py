from .models import City
from django.shortcuts import render
import requests
import datetime


def index(request):
    url = 'https://api.openweathermap.org/data/2.5/weather?q={}&units=metric' \
          '&lang=fr&appid=83e4a44c491d71a05757e7679b2b9f65'
    weather_data = []

    def get_date(timezone):
        tz = datetime.timezone(datetime.timedelta(seconds=int(timezone)))
        return datetime.datetime.now(tz=tz).strftime("%m/%d/%Y, %H:%M")

    cities = City.objects.all()
    for city in cities:
        city_weather = requests.get(url.format(city)).json()
        weather = {
            'city': f'{city}',
            'country': f'{city_weather["sys"]["country"]}',
            'temperature': f'{round(city_weather["main"]["temp"], 1)}',
            'description': f'{city_weather["weather"][0]["description"]}',
            'icon': f'{city_weather["weather"][0]["icon"]}',
            'wind_speed': f'{city_weather["wind"]["speed"]}',
            'humidity': f'{city_weather["main"]["humidity"]}',
            'timezone': f'{get_date(city_weather["timezone"])}'
        }
        weather_data.append(weather)
    print("weather_data")
    print(weather_data)
    context = {'weather_date': weather_data}
    # print(city_weather)
    return render(request, 'weather/index.html', context)
