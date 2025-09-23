import requests
from django.shortcuts import render
from . forms import CityForm
from django.conf import settings

# Create your views here.
def index(request):
    weather_data = None
    default_city = "Delhi"
    api_key = settings.OPENWEATHER_API_KEY

    if request.method == 'POST':
        form = CityForm(request.POST)

        if form.is_valid():
            city = form.cleaned_data['city']
        else:
            city = default_city
    else:
        form = CityForm()
        city = default_city

    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    response = requests.get(url).json()

    if response.get('cod') == 200:
        weather_data = {
                    'city': city,
                    'temperature': round(response['main']['temp']),
                    'description': response['weather'][0]['description'],
                    'icon': response['weather'][0]['icon'],
                    'humidity': response['main']['humidity'],
                   'wind': round(response['wind']['speed'] * 3.6, 1) # convert to km/h,
                }

    else:
        weather_data = {'error': "City not found!"}
        

    return render(request, 'index.html', {'form': form, 'weather_data': weather_data})