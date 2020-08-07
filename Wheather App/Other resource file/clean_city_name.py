import time

with open(r'current.city.list.min.json','r',errors='ignore') as file:
    data = file.read()

import re

# https://regex101.com/r/CoHvtm/1

regex = re.compile(r'name\":\"(\w+(?:\.?)(?: ?)\w+)\"')
cleaned_data = re.findall(regex, data)

import pickle

with open('city_names.pkl','wb') as f:
    pickle.dump(cleaned_data,f)

print(cleaned_data)
time.sleep(1000)