import time
import csv
import os

import datetime as dt

from data_holders import ZTM_bus, bus_stop, bus_for_stop, bus_schedule_entry, bus_route_entry
import requests


class data_reader:
    api_key: str
    bus_data: dict
    bus_stop_data: dict
    busses_for_stops: dict
    schedules: dict
    streets: dict
    bus_routes: dict

    def __init__(self, api_key):
        self.api_key = api_key
        self.bus_data = {}
        self.bus_stop_data = {}
        self.busses_for_stops = {}
        self.schedules = {}
        self.streets = {}
        self.bus_routes = {}

    def time_parser(self, time_data):
        if time_data[:2] == '24':
            time_data = '00' + time_data[2:]
        elif time_data[:2] == '25':
            time_data = '01' + time_data[2:]
        elif time_data[:2] == '26':
            time_data = '02' + time_data[2:]
        elif time_data[:2] == '27':
            time_data = '03' + time_data[2:]
        elif time_data[:2] == '28':
            time_data = '04' + time_data[2:]
        elif time_data[:2] == '29':
            time_data = '05' + time_data[2:]

        return time_data

    def get_bus_data(self, nr_of_samples, sample_length):
        for i in range(nr_of_samples):
            response = response = requests.post(
                'https://api.um.warszawa.pl/api/action/busestrams_get/?resource_id= f2e5503e-' +
                '927d-4ad3-9500-4ab9e55deb59&apikey=' + self.api_key + '&type=1')
            for j in range(len(response.json()['result'])):
                helper = (response.json()['result'][j])
                # print(response.json()['result'])
                time_data = self.time_parser(helper['Time'])
                bus = ZTM_bus(helper['Lines'], helper['Lon'], helper['Lat'], helper['VehicleNumber'],
                              helper['Brigade'], dt.datetime.strptime(time_data, "%Y-%m-%d %H:%M:%S"))

                if helper['Lines'] in self.bus_data:
                    self.bus_data[helper['Lines']].append(bus)
                else:
                    self.bus_data[helper['Lines']] = [bus]

            time.sleep(sample_length)

    def dump_bus_data(self, file_to_dump):
        data_headers = ['Lines', 'Longitude', 'Latitude', 'Street_name', 'VehicleNumber', 'Brigade', 'Time']
        print('gex')
        with open(file_to_dump, 'w', newline='', encoding='utf16') as file:
            print('dex')
            csv_writer = csv.writer(file)
            csv_writer.writerow(data_headers)
            for key in self.bus_data:
                for value in self.bus_data[key]:
                    value.location.find_street()
                    csv_writer.writerow(value.to_csv())

    def get_stops_data(self):
        response = requests.post(
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

    def get_busses_for_stops(self, bus_stop_list_file):
        with open(bus_stop_list_file, 'r', encoding='utf16') as file:
            csv_reader = csv.reader(file)
            nr_of_lines = 0
            for line in csv_reader:
                nr_of_lines = nr_of_lines + 1
                if nr_of_lines > 1 and line[2] != 'null' and line[3] != 'null':
                    response = requests.post(
                        'https://api.um.warszawa.pl/api/action/dbtimetable_get/?id=88cd555f-6f31-43ca-9de4-66c479ad5942&busstopId=' +
                        line[2] + '&busstopNr=' + line[3] + '&apikey=' + self.api_key)
                    for data in response.json()['result']:
                        bus = bus_for_stop(line[2], line[3], data['values'][0]['value'])
                        if len(bus.bus) == 3:
                            if bus.team in self.busses_for_stops:
                                self.busses_for_stops[bus.team].append(bus)
                            else:
                                self.busses_for_stops[bus.team] = [bus]

    def dump_busses_for_stops(self, file_to_dump):
        data_headers = ['Team', 'Post', 'Bus']
        with open(file_to_dump, 'w', newline='', encoding='utf16') as file:
            csv_writer = csv.writer(file)
            csv_writer.writerow(data_headers)
            csv_writer.writerow(data_headers)
            for key in self.busses_for_stops:
                for data in self.busses_for_stops[key]:
                    csv_writer.writerow(data.to_csv())

    def get_bus_schedules(self, busses_for_stops_file):
        with open(busses_for_stops_file, 'r', encoding='utf16') as file:
            csv_reader = csv.reader(file)
            nr_of_lines = 0
            for line in csv_reader:
                nr_of_lines = nr_of_lines + 1
                if nr_of_lines > 1 and len(line) == 3:
                    response = requests.post(
                        'https://api.um.warszawa.pl/api/action/dbtimetable_get/?id=e923fa0e-d96c-43f9-ae6e-60518c9f3238&busstopId=' +
                        line[0] + '&busstopNr=' + line[1] + '&line=' + line[2] + '&apikey=' + self.api_key)
                    #print(response.json())
                    for data in response.json()['result']:
                        time_data = self.time_parser(data['values'][5]['value'])
                        scl = bus_schedule_entry(data['values'][2]['value'], data['values'][3]['value'],
                                                 data['values'][4]['value'],
                                                 dt.datetime.strptime(time_data, "%H:%M:%S"))
                        if line[0] in self.schedules:
                            if line[1] in self.schedules[line[0]]:
                                if line[2] in self.schedules[line[0]][line[1]]:
                                    self.schedules[line[0]][line[1]][line[2]].append(scl)
                                else:
                                    self.schedules[line[0]][line[1]][line[2]] = [scl]
                            else:
                                self.schedules[line[0]][line[1]] = {line[2]: [scl]}
                        else:
                            self.schedules[line[0]] = {line[1]: {line[2]: [scl]}}

    def dump_schedules(self):
        data_headers = ['Brigade', 'Direction', 'Route', 'Time']
        if not os.path.isdir('schedules'):
            os.mkdir('schedules')
        for team in self.schedules:
            for post in self.schedules[team]:
                for bus in self.schedules[team][post]:
                    with open('schedules/' + team + '_' + post + '_' + bus + '.csv', 'w',
                              newline='', encoding='utf16') as file:
                        csv_writer = csv.writer(file)
                        csv_writer.writerow(data_headers)
                        for data in self.schedules[team][post][bus]:
                            csv_writer.writerow(data.to_csv())

    def get_bus_routes(self):
        response = requests.post(
            'https://api.um.warszawa.pl/api/action/public_transport_routes/?apikey=' + self.api_key)
        iterator = 0
        print('sex')
        for bus_nr in response.json()['result']:
            if iterator == 2: break
            for route_type in response.json()['result'][bus_nr]:
                max_nr = 0
                #print(response.json()['result'][bus_nr][route_type])
                for nr in response.json()['result'][bus_nr][route_type]:
                    #print(nr)
                    if int(nr) > max_nr:
                        max_nr = int(nr)
                #print(max_nr)
                if bus_nr not in self.bus_routes:
                    self.bus_routes[bus_nr] = {}
                self.bus_routes[bus_nr][route_type] = {}
                for i in range(max_nr):
                    self.bus_routes[bus_nr][route_type][i + 1] = None
                for nr in response.json()['result'][bus_nr][route_type]:
                    helper = response.json()['result'][bus_nr][route_type][nr]
                    self.bus_routes[bus_nr][route_type][int(nr)] = (
                        bus_route_entry(bus_nr, route_type, helper['ulica_id'], helper['nr_zespolu'],
                                        helper['typ'], helper['nr_przystanku']))
                iterator += 1

    def dump_bus_routes(self, file_to_dump):
        data_headers = ['Route_code', 'Street_id', 'Team_nr', 'Type', 'Bus_stop_nr']
        with open(file_to_dump, 'w', newline='', encoding='utf16') as file:
            csv_writer = csv.writer(file)
            csv_writer.writerow(data_headers)
            for bus_nr in self.bus_routes:
                for route_type in self.bus_routes[bus_nr]:
                    for data in self.bus_routes[bus_nr][route_type]:
                        csv_writer.writerow(self.bus_routes[bus_nr][route_type][data].to_csv())



