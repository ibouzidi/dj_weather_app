from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages
from django.shortcuts import render, redirect, HttpResponse
from .forms import CityForm
from .models import City
from django.shortcuts import render
import requests
import datetime


def index(request):
    """
    A function used display all cities weather stored in the database.
    :param request:Contains information about current user.
    :return:Returns a render function with 3 arguments:
        1.A str 'requests' contains information about current user.
        2.An url that will be used to generate the access page.
        3.A dictionary that contains 2 keys:
            3.1.'weather' that contains data of the weather
            3.2.'form' that contains the generated form.
    """
    url = 'https://api.openweathermap.org/data/2.5/weather?q={}&units=metric' \
          '&lang=fr&appid=83e4a44c491d71a05757e7679b2b9f65'
    weather_data = []

    # Get the date and hours with the local timezone.
    def get_date(timezone):
        tz = datetime.timezone(datetime.timedelta(seconds=int(timezone)))
        return datetime.datetime.now(tz=tz).strftime("%A, %H:%M")

    cities = City.objects.values('pk', 'name')
    for city in cities:
        city_weather = requests.get(url.format(city["name"])).json()
        weather = {
            'pk': f'{city["pk"]}',
            'city': f'{city["name"]}',
            'country': f'{city_weather["sys"]["country"]}',
            'temperature': f'{round(city_weather["main"]["temp"])}',
            'description': f'{city_weather["weather"][0]["description"]}',
            'icon': f'{city_weather["weather"][0]["icon"]}',
            'wind_speed': f'{city_weather["wind"]["speed"]}',
            'humidity': f'{city_weather["main"]["humidity"]}',
            'timezone': f'{get_date(city_weather["timezone"])}'
        }
        weather_data.append(weather)
    # form begin
    if request.method == 'POST':
        form = CityForm(request.POST)
        city_name = request.POST.get('name').capitalize()
        if form.is_valid():
            form.save(commit=False)
            form.save()
            messages.success(request,
                             f'The city {city_name} has been created')
            return redirect('weather:weather_index')
        else:
            context = {'weather_date': weather_data, 'form': form}
            messages.error(request, f'{form.errors}'
                           .replace('<ul class="errorlist"><li>', ' ')
                           .replace('</li></ul>', ''))
            return render(request, 'weather/index.html', context)
    else:
        form = CityForm()
        context = {'weather_date': weather_data, 'form': form}
        return render(request, 'weather/index.html', context)


def city_detail(request, pk=None):
    """
     A function used display information of a specified city weather.
     :param request:Contains information about current user.
     :return:Returns a render function with 3 arguments:
         1.A str 'requests' contains information about current user.
         2.An url that will be used to generate the access page.
         3.A dictionary that contains 3 keys:
             3.1.'weather' that contains weather data of a city.
             3.2.'city' that contains the name of the city in database.
             3.3.'day_weather' that contain a weather forcast of a city.
     """
    try:
        city = City.objects.get(pk=pk)
        url = 'https://api.openweathermap.org/data/2.5/weather?q={}&' \
              'units=metric&lang=fr&appid=83e4a44c491d71a05757e7679b2b9f65'
        url_forcast = 'https://api.openweathermap.org/data/2.5/forecast?q={}&' \
                  'units=metric&cnt=7&lang=fr&appid=' \
                  '83e4a44c491d71a05757e7679b2b9f65'
        weather_data = []
        city_weather = requests.get(url.format(city.name)).json()
        city_forcast_day = requests.get(url_forcast.format(city.name)).json()

        def get_date(timezone):
            tz = datetime.timezone(datetime.timedelta(seconds=int(timezone)))
            return datetime.datetime.now(tz=tz).strftime("%A, %H:%M")

        forcast_weather = []
        for day in city_forcast_day["list"]:
            date = datetime.datetime.fromtimestamp(day['dt'])
            day_icon = day["weather"][0]["icon"]
            day_date = date.strftime("%A, %H:%M")
            day_temp = day["main"]["temp"]
            forcast_weather.append([day_date, day_temp, day_icon])
        weather = {
            'pk': f'{city.pk}',
            'city': f'{city.name}',
            'country': f'{city_weather["sys"]["country"]}',
            'temperature': f'{round(city_weather["main"]["temp"])}',
            'temp_max': f'{round(city_weather["main"]["temp_max"])}',
            'temp_min': f'{round(city_weather["main"]["temp_min"])}',
            'description': f'{city_weather["weather"][0]["description"]}',
            'icon': f'{city_weather["weather"][0]["icon"]}',
            'wind_speed': f'{city_weather["wind"]["speed"]}',
            'humidity': f'{city_weather["main"]["humidity"]}',
            'timezone': f'{get_date(city_weather["timezone"])}',
        }
        weather_data.append(weather)
        context = {
            'weather_date': weather_data,
            'city': city,
            'forcast_weather': forcast_weather
        }
        return render(request, 'weather/city_detail.html', context)
    except ObjectDoesNotExist:
        messages.error(request, 'No city with that id')
        return redirect('weather:weather_index')