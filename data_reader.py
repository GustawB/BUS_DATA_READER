import time
import csv

from datetime import datetime

from data_holders import ZTM_bus, bus_stop
import requests


class data_reader:
    api_key: str
    bus_data: dict
    bus_stop_data: dict

    def __init__(self, api_key):
        self.api_key = api_key
        self.bus_data = {}
        self.bus_stop_data = {}

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

    def dump_bus_data(self, file_to_dump):
        data_headers = ['Lines', 'Longitude', 'Latitude', 'VehicleNumber', 'Brigade', 'Time']
        with open(file_to_dump, 'w', newline='', encoding='utf16') as file:
            csv_writer = csv.writer(file)
            csv_writer.writerow(data_headers)
            for key in self.bus_data:
                for value in self.bus_data[key]:
                    csv_writer.writerow(value.to_csv())

        self.bus_data.clear()

    def get_stops_data(self):
        response = response = requests.post(
            'https://api.um.warszawa.pl/api/action/dbstore_get/?id=ab75c33d-3a26-4342-b36a-6e5fef0a3ac3&page=1')
        for data in response.json()['result']:
            bs = bus_stop(data['values'][2]['value'], data['values'][3]['value'], data['values'][0]['value'],
                          data['values'][1]['value'], data['values'][6]['value'],
                          float(data['values'][5]['value']), float(data['values'][4]['value']))

            if bs.team_name in self.bus_stop_data:
                self.bus_stop_data[bs.team_name].append(bs)
            else:
                self.bus_stop_data[bs.team_name] = [bs]

            print(data['values'])

    def dump_stops_data(self, file_to_dump):
        data_headers = ['Team_name', 'Street_id', 'Team', 'Post', 'Direction', 'Longitude', 'Latitude']
        with open(file_to_dump, 'w', newline='', encoding='utf16') as file:
            csv_writer = csv.writer(file)
            csv_writer.writerow(data_headers)
            for key in self.bus_stop_data:
                for value in self.bus_stop_data[key]:
                    csv_writer.writerow(value.to_csv())
