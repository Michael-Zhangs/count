import json
import os
from datetime import datetime

class Type():

    def __init__(self):
        pass

    def set_value(self, power, water):
        self.power = power
        self.water = water

class Floor():

    def __init__(self):
        self.last = Type()
        self.present = Type()

    def count_delta(self):
        self.powerdelta = self.present.power - self.last.power
        self.waterdelta = self.present.water - self.last.water

def get_last(get_first, get_second):
    power = input('The last value of power of the first floor: ')
    water = input('The last value of water of the first floor: ')
    power = float(power)
    water = float(water)
    get_first.last.set_value(power, water)
    power = input('The last value of power of the second floor: ')
    water = input('The last value of water of the second floor: ')
    power = float(power)
    water = float(water)
    get_second.last.set_value(power, water)

def get_present(get_first, get_second):
    power = input('The present value of power of the first floor: ')
    water = input('The present value of water of the first floor: ')
    power = float(power)
    water = float(water)
    get_first.present.set_value(power, water)
    power = input('The present value of power of the second floor: ')
    water = input('The present value of water of the second floor: ')
    power = float(power)
    water = float(water)
    get_second.present.set_value(power, water)

def save_data(get_building, get_first, get_second):
    dt=datetime.now()
    try:
        with open('data.json') as f_data:
            data_save = json.load(f_data)
    except FileNotFoundError:
        data_save = {'building': {building: {'first': {}, 'second': {}}}}
    try:
        temp = data_save['building'][building]
    except KeyError:
        data_save['building']={}
        data_save['building'][building]={'first': {}, 'second': {}}
    data_save['building'][building]['first']['power'] = get_first.present.power
    data_save['building'][building]['first']['water'] = get_first.present.water
    data_save['building'][building]['second']['power'] = get_second.present.power
    data_save['building'][building]['second']['water'] = get_second.present.water
    data_save['building'][building]['date'] = dt.strftime( '%Y-%m-%d %H:%M:%S %f' )
    data_save['date'] = dt.strftime( '%Y-%m-%d_%H:%M:%S_%f' )
    with open('data.json', 'w') as f_data:
        json.dump(data_save, f_data)

def backup():
    try:
        with open('data.json') as f_data:
            data_temp = json.load(f_data)
    except FileNotFoundError:
        pass
    else:
        try:
            with open('backup/'+data_temp['date']+'.json', 'w') as f_data:
                json.dump(data_temp, f_data)
        except FileNotFoundError:
            os.mkdir('backup')
            with open('backup/'+data_temp['date']+'.json', 'w') as f_data:
                json.dump(data_temp, f_data)

data = {}
first = Floor()
second = Floor()

building = input('The name of the building: ')

try:
    with open('data.json') as f_data:
        data = json.load(f_data)
        data = data['building'][building]
except KeyError:
    get_last(first, second)
except FileNotFoundError:
    get_last(first, second)
else:
    flag = input('Use data from '+data['date']+' ? (Y/N): ')
    if not (flag == 'Y' or flag == 'y'):
        get_last(first, second)
    else:
        first.last.set_value(data['first']['power'], data['first']['water'])
        second.last.set_value(data['second']['power'], data['second']['water'])
get_present(first, second)

first.count_delta()
second.count_delta()

payment_power = input('The payment of power: ')
payment_water = input('The payment of water: ')
payment_power = float(payment_power)
payment_water = float(payment_water)

payment_first_power = first.powerdelta / (first.powerdelta + second.powerdelta) * payment_power
payment_first_water = first.waterdelta / (first.waterdelta + second.waterdelta) * payment_water

payment_second_power = second.powerdelta / (first.powerdelta + second.powerdelta) * payment_power
payment_second_water = second.waterdelta / (first.waterdelta + second.waterdelta) * payment_water

print('\n')
print('The payment of power of the first floor: ' + str(payment_first_power))
print('The payment of water of the first floor: ' + str(payment_first_water))

print('The payment of power of the second floor: ' + str(payment_second_power))
print('The payment of water of the second floor: ' + str(payment_second_water))

print('\n')
print('The total payment of the first floor: ' + str(payment_first_power + payment_first_water))
print('The total payment of the scond floor: ' + str(payment_second_power + payment_second_water))

backup()
save_data(building, first, second)
