from django.shortcuts import render
import requests
import datetime


def index(request):
    url = 'https://api.openweathermap.org/data/2.5/weather?q={}&units=metric' \
          '&lang=fr&appid=83e4a44c491d71a05757e7679b2b9f65'
    city = 'Saint-Étienne'
    city_weather = requests.get(url.format(city)).json()

    def get_date(timezone):
        tz = datetime.timezone(datetime.timedelta(seconds=int(timezone)))
        return datetime.datetime.now(tz=tz).strftime("%m/%d/%Y, %H:%M")

    weather = {
        'city': f'{city}',
        'country': f'{city_weather["sys"]["country"]}',
        'temperature': f'{city_weather["main"]["temp"]}',
        'description': f'{city_weather["weather"][0]["description"]}',
        'icon': f'{city_weather["weather"][0]["icon"]}',
        'wind_speed': f'{city_weather["wind"]["speed"]}',
        'humidity': f'{city_weather["main"]["humidity"]}',
        'timezone': f'{get_date(city_weather["timezone"])}'
    }
    context = {'weather': weather}
    print(city_weather)
    return render(request, 'weather/index.html', context)
