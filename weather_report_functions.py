# Import the library.
import datetime
import time
import requests

# import os

# Define API keys
# Hard coded values included for sake of marking
API_key = "Key"  # os.environ.get('OpenWeather_API_Key')
G_API_key = "Key"  # os.environ.get('Google_Maps_API_Key')


# Returns json Latitude + Longitude coordinates from given location via Google Maps API, text location input
# Will return single object with both latitude and longitude methods, needs to be separated before use
def coordinates(location):
    location = replace_text(location, " ", "+")
    geo_url = "https://maps.googleapis.com/maps/api/geocode/json?address="+location+"&key="+G_API_key
    response = requests.get(geo_url)
    response_code_error(response)
    return response.json()["results"][0]["geometry"]["location"]


# Returns json weather data for given location via OpenWeather API, needs latitude and longitude input
def weather(location):
    latitude = str(coordinates(location)["lat"])
    longitude = str(coordinates(location)["lng"])

    # current weather data API with current date info
    #weather_url = "https://api.openweathermap.org/data/2.5/weather?lat="+latitude+"&lon="+longitude+"&appid="+API_key

    # One call api with 8 day forecast
    weather_url = ("https://api.openweathermap.org/data/3.0/onecall?lat=" + latitude + "&lon=" + longitude +
                   "&exclude=current,hourly,minutely,alerts&appid=" + API_key)
    response = requests.get(weather_url)
    response_code_error(response)
    return response.json()


# To replace text for link compatibility
def replace_text(text, to_replace, replace_with):
    text = text.replace(to_replace, replace_with)
    return text


# HTTP response code error handling for API requests
def response_code_error(response):
    if response.status_code == 200:
        return
    else:
        print("Sorry, something went wrong.\n Error " + str(response.status_code))


# Convert Kelvin to Celsius
def kelvin_to_celsius(temp):
    return int(temp - 273.15)


# Weather report class to hold all provided weather information
class WeatherReport:
    def __init__(self, temp, temp_max, temp_min, description, humidity, wind, date, future_forecast):
        self.temp = temp
        self.temp_max = temp_max
        self.temp_min = temp_min
        self.description = description
        self.humidity = humidity
        self.wind = wind
        self.date = date
        self.future_forecast = future_forecast


# Extract and store required weather data from weather function
def create_weather_report(location):
    weather_info = weather(location)

    # initiate empty str array, i=1 to signify tomorrow
    future_forecast = [""]*7
    i = 1

    # Retrieve in depth info for first date, today
    temp = kelvin_to_celsius(weather_info["daily"][0]["temp"]["day"])
    temp_max = kelvin_to_celsius(weather_info["daily"][0]["temp"]["max"])
    temp_min = kelvin_to_celsius(weather_info["daily"][0]["temp"]["min"])
    description = weather_info["daily"][0]["summary"]
    humidity = weather_info["daily"][0]["humidity"]
    wind = weather_info["daily"][0]["wind_speed"]
    date = datetime.date.fromtimestamp(weather_info["daily"][0]["dt"])

    # Loops through next seven days to retrieve basic info, stores in array
    while i < len(weather_info["daily"]):
        # adds i value to date for new date value
        future_forecast[(i-1)] = (str((date+datetime.timedelta(i)).strftime("%d/%m/%Y")) + " " +
                            str(kelvin_to_celsius(weather_info["daily"][i]["temp"]["day"])) + "\N{DEGREE SIGN}C " +
                              str(weather_info["daily"][i]["weather"][0]["description"])
                              )
        i += 1

    date = date.strftime("%d/%m/%Y")
    # Store all weather information in Weather Report class
    report = WeatherReport(temp, temp_max, temp_min, description, humidity, wind, date, future_forecast)
    return report


# Displays weather report in easy to read text
def display_report_overview(location):
    report = create_weather_report(location)
    overview = "The forecasted weather for "+location+" today "+str(report.date)+" is "+report.description+" with a humidity level of "+str(
        report.humidity) + "% and a wind speed of " + str(report.wind) + "m/s."
    return overview


# Displays weather report in easy to read text
def display_report_temp(location):
    report = create_weather_report(location)
    temp = "The current temperature is " + str(report.temp) + "\N{DEGREE SIGN}C, with a maximum of " + str(
        report.temp_max) + "\N{DEGREE SIGN}C, and a minimum of " + str(report.temp_min) + "\N{DEGREE SIGN}C."
    return temp

def display_report_future(location):
    report = create_weather_report(location)
    report_future = str(report.future_forecast[0]+", "+report.future_forecast[1]+", "+report.future_forecast[2]+", "+
    report.future_forecast[3]+", "+report.future_forecast[4]+", "+report.future_forecast[5]+", "+report.future_forecast[6])
    return report_future
