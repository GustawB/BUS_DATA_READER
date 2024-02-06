import time
from datetime import datetime

from data_holders import ZTM_bus
import requests


class data_reader:
    nr_of_samples: int
    sample_length: int
    api_key: str
    read_data: dict

    def __init__(self, nr_of_samples, sample_length, api_key):
        self.nr_of_samples = nr_of_samples
        self.sample_length = sample_length
        self.api_key = api_key
        self.read_data = {}

    def get_bus_data(self):
        for i in range(self.nr_of_samples):
            response = response = requests.post('https://api.um.warszawa.pl/api/action/busestrams_get/?resource_id= f2e5503e-' +
                                                '927d-4ad3-9500-4ab9e55deb59&apikey=' + self.api_key + '&type=1')
            for j in range(len(response.json()['result'])):
                helper = response.json()['result'][j]
                bus = ZTM_bus(helper['Lines'], helper['Lon'], helper['Lat'], helper['VehicleNumber'],
                              helper['Brigade'], datetime.strptime(helper['Time'], "%Y-%m-%d %H:%M:%S"))

                if helper['Lines'] in self.read_data:
                    self.read_data[helper['Lines']].append(bus)
                else:
                    self.read_data[helper['Lines']] = [bus]

            time.sleep(self.sample_length)
