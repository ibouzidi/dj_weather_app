from django.urls import path
from . import views

app_name = "weather"

urlpatterns = [
    path('', views.index, name="weather_index"),
    path('weather/city/<int:pk>/detail', views.city_detail,
         name="city_detail")
]