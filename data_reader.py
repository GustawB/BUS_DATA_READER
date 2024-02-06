import time
import csv

from datetime import datetime

from data_holders import ZTM_bus
import requests


class data_reader:
    api_key: str
    bus_data: dict
    busstop_data: dict

    def __init__(self, api_key):
        self.api_key = api_key
        self.bus_data = {}
        self.busstop_data = {}

    def get_bus_data(self, nr_of_samples, sample_length):
        for i in range(nr_of_samples):
            response = response = requests.post(
                'https://api.um.warszawa.pl/api/action/busestrams_get/?resource_id= f2e5503e-' +
                '927d-4ad3-9500-4ab9e55deb59&apikey=' + self.api_key + '&type=1')
            for j in range(len(response.json()['result'])):
                helper = response.json()['result'][j]
                bus = ZTM_bus(helper['Lines'], helper['Lon'], helper['Lat'], helper['VehicleNumber'],
                              helper['Brigade'], datetime.strptime(helper['Time'], "%Y-%m-%d %H:%M:%S"))

                if helper['Lines'] in self.bus_data:
                    self.bus_data[helper['Lines']].append(bus)
                else:
                    self.bus_data[helper['Lines']] = [bus]

            time.sleep(sample_length)

    def dump_bus_data(self):
        data_headers = ['Lines', 'Longitude', 'Latitude', 'VehicleNumber', 'Brigade', 'Time']
        with open('bus_data.csv', 'w', newline='') as file:
            csv_writer = csv.writer(file)
            csv_writer.writerow(data_headers)
            for key in self.bus_data:
                for value in self.bus_data[key]:
                    csv_writer.writerow(value.to_csv())

        self.bus_data.clear()


    def get_stops_data(self):
        response = response = requests.post('https://api.um.warszawa.pl/api/action/dbstore_get/?id=ab75c33d-3a26-4342-b36a-6e5fef0a3ac3&page=1')
        print(response.json())
