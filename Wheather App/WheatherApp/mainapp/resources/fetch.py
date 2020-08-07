from bs4 import BeautifulSoup as bs
from urllib.request import urlopen
import json
from datetime import datetime
from dateutil import tz

class API():
    def __init__(self, user_pref, is_location_set=0):
        self.__is_location_set = is_location_set

        if self.__is_location_set:
            user_pref = self.__set_user_inf(user_pref)
            self.__latitude = user_pref['latitude']
            self.__longitude = user_pref['longitude']
        else:
            self.__city_name = user_pref['city_name'].replace(' ','%20')

        self.api_key = 'your_api'
        self.__unit = user_pref['unit']
        self.__language = user_pref['language']
        self.__tz = user_pref['tz']

    def __set_user_inf(self, ajax_data):
        # This function is to clean data from query dictionary
        user_pref = {}
        user_pref['unit'] = ajax_data['pref[unit]']
        user_pref['language'] = ajax_data['pref[language]']
        user_pref['tz'] = ajax_data['pref[tz]']
        user_pref['latitude'] = ajax_data['location[latitude]']
        user_pref['longitude'] = ajax_data['location[longitude]']
        return user_pref

    def __fetch_url(self):
        '''
        city_name = Wheather of city_name will be displayed.
        unit = If unit is 'standard' then temperature will be in Kelvin, 
               if 'metric' then it will be in Celsius,
               if 'inperial' then it will be in Fahrenheit.
        language = Your prefered laguage.
        pref_tz = Your prefered timezone for formatting your sunset, sunrise time.
        '''
        if self.__is_location_set:
            req = urlopen(f'https://api.openweathermap.org/data/2.5/weather?lat={self.__latitude}&lon={self.__longitude}&appid={self.api_key}&units={self.__unit}&lang={self.__language}')
        else:
            req = urlopen(f'https://api.openweathermap.org/data/2.5/weather?q={self.__city_name}&appid={self.api_key}&units={self.__unit}&lang={self.__language}')

        return json.loads(req.read())
    
    def wheather_data(self):
        '''This method is to get a dictionary of all the required wheather data'''
        r = self.__fetch_url()  # raw json data
        wh_param = {}
        wh_param['type_of_wheather'] = r['weather'][0]['main']  #for changing image background
        wh_param['wheather_description_for_user'] = r['weather'][0]['description']
        wh_param['temperature'] = r['main']['feels_like']
        wh_param['humidity'] = r['main']['humidity']
        wh_param['min_temperature'] = r['main']['temp_min']
        wh_param['max_temperature'] = r['main']['temp_max']
        wh_param['wind_speed'] = r['wind']['speed']
        wh_param['wind_direction'] = r['wind']['deg']  # in degrees metrological(? symbol in page)
        wh_param['cloudiness'] = r['clouds']['all']  #value in percent
        wh_param['city'] = r['name']
        wh_param['visibility'] = r['visibility']
        wh_param['sunrise'] = r['sys']['sunrise']
        wh_param['sunset'] = r['sys']['sunset']
        wh_param['time_of_update_utc'] = r['dt']

        utc_time = [wh_param['sunrise'],wh_param['sunset'],wh_param['time_of_update_utc']]
        utc_time_str = ['sunrise','sunset','time_of_update_time']
        converted_time = {}
        for i,j in list(zip(utc_time,utc_time_str)):
            time = datetime.fromtimestamp(i).astimezone(tz.gettz(self.__tz))
            converted_time[j] = str(time.strftime('%X'))
            if j=='time_of_update_time':
                converted_time['time_of_update_day'] = time.strftime('%x')
                
        for i in converted_time:
            wh_param[i] = converted_time[i]

        return wh_param