import csv
import math
import requests


def update_data():
    with open('country-list.csv', 'r') as fileAPI:
        readerAPI = csv.reader(fileAPI)
        with open('citiesData.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['index',
                             'capital city',
                             'temperature [°C]',
                             'pressure [hPa]',
                             'humidity [%]',
                             'visibility',
                             'wind speed [m/s]',
                             'clouds [%]',
                             'rain in last hour [mm]',
                             'snow in last hour [mm]'])
            index = 1
            for row in readerAPI:
                capitalCity = row[1]
                url = (f'https://api.openweathermap.org/data/2.5/weather?q={capitalCity}&limit=1'
                       f'&appid=6681af215dc7936e8fdb9e2ee497f649')
                response = requests.get(url)

                if response.status_code == 200:
                    temperature = math.floor(float(response.json().get('main', [])['temp']) - 273.15)
                    pressure = response.json().get('main', [])['pressure']
                    humidity = response.json().get('main', [])['humidity']
                    visibility = response.json().get('visibility', [])
                    windSpeed = response.json().get('wind', [])['speed']
                    clouds = response.json().get('clouds', [])['all']
                    rainInLastHour = response.json().get('rain', [])['1h'] if bool(
                        response.json().get('rain', [])) else 0
                    snowInLastHour = response.json().get('snow', [])['1h'] if bool(
                        response.json().get('snow', [])) else 0

                    print(index, capitalCity, temperature, pressure, humidity, visibility, windSpeed, clouds,
                          rainInLastHour, snowInLastHour)
                    writer.writerow([index, capitalCity, temperature, pressure, humidity, visibility, windSpeed, clouds,
                                     rainInLastHour, snowInLastHour])
                    index = index + 1


updateData = input("Do you want to update the data? (y/n): ").lower()
if updateData == 'y':
    update_data()
value = int(input("Type of parameter?: temperature[0],"
                  " pressure[1],"
                  " humidity[2],"
                  " visibility[3],"
                  " windSpeed[4],"
                  " clouds[5],"
                  " rainInLastHour[6]"
                  " snowInLastHour[7]"))
while value > 7 or value < 0:
    value = int(input("Wrong input: Type of parameter?: temperature[0],"
                      " pressure[1],"
                      " humidity[2],"
                      " visibility[3],"
                      " windSpeed[4],"
                      " clouds[5],"
                      " rainInLastHour[6]"
                      " snowInLastHour[7]"))
minOrMax = int(input('Min value [0] or Max value [1]'))
while minOrMax < 0 or minOrMax > 1:
    minOrMax = int(input('Wrong input: Min value [0] or Max value [1]'))

with open('citiesData.csv', 'r') as csvfile:
    readerCityData = csv.reader(csvfile)

    def get_min(parameter):
        minValue = 1000000.0
        minValueCity = ""
        afterFirstIteration = False
        for city in readerCityData:
            if not afterFirstIteration:
                afterFirstIteration = True
                continue
            elif float(city[parameter + 2]) < float(minValue) or float(city[parameter + 2]) == float(minValue):
                minValue = city[parameter + 2]
                minValueCity = city[1]
        print(minValueCity)

    def get_max(parameter):
        maxValue = -1000000.0
        maxValueCity = ""
        maxTemp = -1000
        maxHum = 0
        afterFirstIteration = False
        for city in readerCityData:
            if not afterFirstIteration:
                afterFirstIteration = True
                continue
            elif float(city[parameter + 2]) > float(maxValue):
                maxValue = city[parameter + 2]
                maxValueCity = city[1]
                if parameter == 2:
                    maxTemp = float(city[2])
                    maxHum = float(city[4])
            elif parameter == 2 and float(city[4]) == maxHum:
                if float(city[2]) > maxTemp:
                    maxValueCity = city[1]
                    maxTemp = float(city[2])
        print(maxValueCity)


    if minOrMax == 0:
        get_min(value)
    else:
        get_max(value)