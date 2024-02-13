import time
import csv
import os
import requests

from buspy.data_holders.data_holders import ZTMBus, BusStop, BusForStop, BusScheduleEntry, BusRouteEntry
import datetime


class DataReader:
    __slots__ = ('__api_key', '__bus_data', '__bus_stop_data', '__buses_for_stops', '__schedules', '__bus_routes')

    def __init__(self, api_key):
        self.__api_key = api_key
        self.__bus_data = {}
        self.__bus_stop_data = {}
        self.__buses_for_stops = {}
        self.__schedules = {}
        self.__bus_routes = {}

    @property
    def api_key(self):
        return self.__api_key

    @property
    def bus_data(self):
        return self.__bus_data

    @property
    def bus_stop_data(self):
        return self.__bus_stop_data

    @property
    def buses_for_stops(self):
        return self.__buses_for_stops

    @property
    def schedules(self):
        return self.__schedules

    @property
    def bus_routes(self):
        return self.__bus_routes

    @staticmethod
    def time_parser(time_data):
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
        url = ('https://api.um.warszawa.pl/api/action/busestrams_get/?resource_id= '
               'f2e5503e-927d-4ad3-9500-4ab9e55deb59&apikey=') + self.__api_key + '&type=1'
        for i in range(nr_of_samples):
            response = requests.get(url)
            while response.status_code != 200 or response.json()['result'][0] == 'B':
                response = requests.get(url)
            for j in range(len(response.json()['result'])):
                helper = response.json()['result'][j]
                time_data = self.time_parser(helper['Time'])
                if helper['Lines'][0] != 'Z':
                    bus = ZTMBus(helper['Lines'], helper['Lon'], helper['Lat'], helper['VehicleNumber'],
                                 helper['Brigade'], time_data)

                    if helper['Lines'] in self.__bus_data:
                        self.__bus_data[helper['Lines']].append(bus)
                    else:
                        self.__bus_data[helper['Lines']] = [bus]

            time.sleep(sample_length)

    def dump_bus_data(self, file_to_dump, time_offset=-1):
        time_data = datetime.datetime.now(datetime.timezone.utc)
        time_in_sec = (time_data.hour + 1) * 60
        time_in_sec += time_data.minute
        time_in_sec *= 60
        time_in_sec += int(time_data.second)
        data_headers = ['Lines', 'Longitude', 'Latitude', 'Street_name', 'VehicleNumber', 'Brigade', 'Time']
        with open(file_to_dump, 'w', newline='', encoding='utf16') as file:
            csv_writer = csv.writer(file)
            csv_writer.writerow(data_headers)
            for key in self.__bus_data:
                for value in self.__bus_data[key]:
                    if 0 < time_offset < abs(value.time_data - time_in_sec):
                        continue
                    value.location.find_street()
                    csv_writer.writerow(value.to_csv())

    def get_stops_data(self):
        response = requests.get(
            'https://api.um.warszawa.pl/api/action/dbstore_get/?id=ab75c33d-3a26-4342-b36a-6e5fef0a3ac3&page=1')
        for data in response.json()['result']:
            bs = BusStop(data['values'][2]['value'], data['values'][3]['value'], data['values'][0]['value'],
                         data['values'][1]['value'], data['values'][6]['value'],
                         float(data['values'][5]['value']), float(data['values'][4]['value']))

            if bs.team_name in self.__bus_stop_data:
                self.__bus_stop_data[bs.team_name].append(bs)
            else:
                self.__bus_stop_data[bs.team_name] = [bs]

            print(data['values'])

    def dump_stops_data(self, file_to_dump):
        data_headers = ['Team_name', 'Street_id', 'Team', 'Post', 'Direction', 'Longitude', 'Latitude']
        with open(file_to_dump, 'w', newline='', encoding='utf16') as file:
            csv_writer = csv.writer(file)
            csv_writer.writerow(data_headers)
            for key in self.__bus_stop_data:
                for value in self.__bus_stop_data[key]:
                    csv_writer.writerow(value.to_csv())

    def get_buses_for_stops(self, bus_stop_list_file):
        with open(bus_stop_list_file, 'r', encoding='utf16') as file:
            csv_reader = csv.reader(file)
            nr_of_lines = 0
            for line in csv_reader:
                nr_of_lines = nr_of_lines + 1
                if nr_of_lines > 1 and line[2] != 'null' and line[3] != 'null':
                    response = requests.get(
                        'https://api.um.warszawa.pl/api/action/dbtimetable_get/?id=88cd555f-6f31-43ca-9de4'
                        '-66c479ad5942&busstopId=' +
                        line[2] + '&busstopNr=' + line[3] + '&apikey=' + self.__api_key)
                    for data in response.json()['result']:
                        bus = BusForStop(line[2], line[3], data['values'][0]['value'])
                        if len(bus.bus) == 3:
                            if bus.team in self.__buses_for_stops:
                                self.__buses_for_stops[bus.team].append(bus)
                            else:
                                self.__buses_for_stops[bus.team] = [bus]

    def dump_buses_for_stops(self, file_to_dump):
        data_headers = ['Team', 'Post', 'Bus']
        with open(file_to_dump, 'w', newline='', encoding='utf16') as file:
            csv_writer = csv.writer(file)
            csv_writer.writerow(data_headers)
            for key in self.__buses_for_stops:
                for data in self.__buses_for_stops[key]:
                    csv_writer.writerow(data.to_csv())

    def get_bus_schedules(self, __buses_for_stops_file):
        with open(__buses_for_stops_file, 'r', encoding='utf16') as file:
            csv_reader = csv.reader(file)
            nr_of_lines = 0
            for line in csv_reader:
                nr_of_lines = nr_of_lines + 1
                if nr_of_lines > 1 and len(line) == 3:
                    response = requests.get(
                        'https://api.um.warszawa.pl/api/action/dbtimetable_get/?id=e923fa0e-d96c-43f9-ae6e'
                        '-60518c9f3238&busstopId=' +
                        line[0] + '&busstopNr=' + line[1] + '&line=' + line[2] + '&apikey=' + self.__api_key)
                    for data in response.json()['result']:
                        time_data = self.time_parser(data['values'][5]['value'])
                        scl = BusScheduleEntry(data['values'][2]['value'], data['values'][3]['value'],
                                               data['values'][4]['value'], time_data)
                        if line[0] in self.__schedules:
                            if line[1] in self.__schedules[line[0]]:
                                if line[2] in self.__schedules[line[0]][line[1]]:
                                    self.__schedules[line[0]][line[1]][line[2]].append(scl)
                                else:
                                    self.__schedules[line[0]][line[1]][line[2]] = [scl]
                            else:
                                self.__schedules[line[0]][line[1]] = {line[2]: [scl]}
                        else:
                            self.__schedules[line[0]] = {line[1]: {line[2]: [scl]}}

    def dump_schedules(self, folder_to_store_in):
        data_headers = ['Brigade', 'Direction', 'Route', 'Time']
        if not os.path.isdir(folder_to_store_in):
            os.mkdir(folder_to_store_in)
        for team in self.__schedules:
            for post in self.__schedules[team]:
                for bus in self.__schedules[team][post]:
                    with open(folder_to_store_in + '/' + team + '_' + post + '_' + bus + '.csv', 'w',
                              newline='', encoding='utf16') as file:
                        csv_writer = csv.writer(file)
                        csv_writer.writerow(data_headers)
                        for data in self.__schedules[team][post][bus]:
                            csv_writer.writerow(data.to_csv())

    def get_bus_routes(self):
        response = requests.get(
            'https://api.um.warszawa.pl/api/action/public_transport_routes/?apikey=' + self.__api_key)
        for bus_nr in response.json()['result']:
            for route_type in response.json()['result'][bus_nr]:
                max_nr = 0
                for nr in response.json()['result'][bus_nr][route_type]:
                    if int(nr) > max_nr:
                        max_nr = int(nr)
                if bus_nr not in self.__bus_routes:
                    self.__bus_routes[bus_nr] = {}
                self.__bus_routes[bus_nr][route_type] = {}
                for i in range(max_nr):
                    self.__bus_routes[bus_nr][route_type][i + 1] = None
                for nr in response.json()['result'][bus_nr][route_type]:
                    helper = response.json()['result'][bus_nr][route_type][nr]
                    self.__bus_routes[bus_nr][route_type][int(nr)] = (
                        BusRouteEntry(bus_nr, route_type, helper['ulica_id'], helper['nr_zespolu'],
                                      helper['typ'], helper['nr_przystanku']))

    def dump_bus_routes(self, file_to_dump):
        data_headers = ['Bus_nr', 'Route_code', 'Street_id', 'Team_nr', 'Type', 'Bus_stop_nr']
        with open(file_to_dump, 'w', newline='', encoding='utf16') as file:
            csv_writer = csv.writer(file)
            csv_writer.writerow(data_headers)
            for bus_nr in self.__bus_routes:
                for route_type in self.__bus_routes[bus_nr]:
                    for data in self.__bus_routes[bus_nr][route_type]:
                        csv_writer.writerow(self.__bus_routes[bus_nr][route_type][data].to_csv())
