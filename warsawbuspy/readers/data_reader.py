import time
import datetime
import csv
import os
import requests

from warsawbuspy.holders.data_holders import ZTMBus, BusStop, BusForStop, BusScheduleEntry, BusRouteEntry


# Class responsible for fetching the data from the https://api.um.warszawa.pl.
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

    # API sends times like 25:01:24 for schedules etc., so this function parses that back
    # into normal time format (for 25:00:00 it would be 01:00:00).
    @staticmethod
    def time_parser(time_data):
        if '24' <= time_data[:2] <= '29':
            time_data = '0' + str(int(time_data[:2]) % 24) + time_data[2:]
        return time_data

    # Function that retrieves data bout bus locations every 'sample_length' seconds 'nr_of_samples' times.
    def get_bus_data(self, nr_of_samples, sample_length, time_offset=-1):
        url = ('https://api.um.warszawa.pl/api/action/busestrams_get/?resource_id= '
               'f2e5503e-927d-4ad3-9500-4ab9e55deb59&apikey=') + self.__api_key + '&type=1'
        time_data = datetime.datetime.now(datetime.timezone.utc)
        time_in_sec = (time_data.hour + 1) * 60
        time_in_sec += time_data.minute
        time_in_sec *= 60
        time_in_sec += int(time_data.second)
        for i in range(nr_of_samples):
            response = requests.get(url)
            while response.status_code != 200 or response.json()['result'][0] == 'B':
                response = requests.get(url)
            for j in range(len(response.json()['result'])):
                helper = response.json()['result'][j]
                time_data = self.time_parser(helper['Time'])
                if helper['Lines'][0] != 'Z':  # Those are replacement buses, and there are problems with them
                    # not having schedules or routes or etc., and there are only four of them, so I ignore them.
                    bus = ZTMBus(helper['Lines'], helper['Lon'], helper['Lat'], helper['VehicleNumber'],
                                 helper['Brigade'], time_data)
                    if 0 < time_offset < abs(bus.time_data - time_in_sec):
                        continue
                    if helper['Lines'] in self.__bus_data:
                        self.__bus_data[helper['Lines']].append(bus)
                    else:
                        self.__bus_data[helper['Lines']] = [bus]
            # Waiting for the next sampling.
            time_in_sec += sample_length
            time.sleep(sample_length)

    # Function that stores all the gathered data about buses locations into the given file.
    # This operation clears all data in the __bus_data dict.
    def dump_bus_data(self, file_to_dump):
        data_headers = ['Lines', 'Longitude', 'Latitude', 'Street_name', 'VehicleNumber', 'Brigade', 'Time']
        with open(file_to_dump, 'w', newline='', encoding='utf16') as file:
            csv_writer = csv.writer(file)
            csv_writer.writerow(data_headers)
            for key in self.__bus_data:
                for value in self.__bus_data[key]:
                    value.location.find_street()
                    csv_writer.writerow(value.to_csv())
        self.__bus_data.clear()

    # Function that retrieves data about every bus stop in the city.
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

    # Function that stores data about bus stops into the given file. This operation clears all data
    # in the __bus_stop_data dict.
    def dump_stops_data(self, file_to_dump):
        data_headers = ['Team_name', 'Street_id', 'Team', 'Post', 'Direction', 'Longitude', 'Latitude']
        with open(file_to_dump, 'w', newline='', encoding='utf16') as file:
            csv_writer = csv.writer(file)
            csv_writer.writerow(data_headers)
            for key in self.__bus_stop_data:
                for value in self.__bus_stop_data[key]:
                    csv_writer.writerow(value.to_csv())
        self.__bus_stop_data.clear()

    # Function that retrieves the information about every bus that goes through every bus stop.
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
                        if len(bus.bus) == 3:  # Checking if what we received is actually a bus number
                            # (e.g. not a tram one)
                            if bus.team in self.__buses_for_stops:
                                self.__buses_for_stops[bus.team].append(bus)
                            else:
                                self.__buses_for_stops[bus.team] = [bus]

    # Function that stores data about bus numbers for every bus stop into the given file.
    # This operation clears every data in the __buses_for_stops dict.
    def dump_buses_for_stops(self, file_to_dump):
        data_headers = ['Team', 'Post', 'Bus']
        with open(file_to_dump, 'w', newline='', encoding='utf16') as file:
            csv_writer = csv.writer(file)
            csv_writer.writerow(data_headers)
            for key in self.__buses_for_stops:
                for data in self.__buses_for_stops[key]:
                    csv_writer.writerow(data.to_csv())
        self.__buses_for_stops.clear()

    # Function that retrieves the bus schedule for every existing combination of bus stop, bus post and bus nr.
    # Those combinations are available i __buses_for_stops_file
    # that should be created by get_buses_for_stops() function.
    def get_bus_schedules(self, __buses_for_stops_file):
        with open(__buses_for_stops_file, 'r', encoding='utf16') as file:
            csv_reader = csv.reader(file)
            nr_of_lines = 0
            for line in csv_reader:  # Going through every combination of bus stop, bus post and bus nr.
                nr_of_lines = nr_of_lines + 1
                if nr_of_lines > 1 and len(line) == 3:  # Diuble checking if we are actually operating with a bus nr.
                    response = requests.get(
                        'https://api.um.warszawa.pl/api/action/dbtimetable_get/?id=e923fa0e-d96c-43f9-ae6e'
                        '-60518c9f3238&busstopId=' +
                        line[0] + '&busstopNr=' + line[1] + '&line=' + line[2] + '&apikey=' + self.__api_key)
                    for data in response.json()['result']:  # Iterating over the received schedule.
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

    # Function that dumps schedules into the given folder. Every schedule is stored in a file
    # with a name build from bus stop team, bus stop post and bus nr. This operation clears
    # every data in the __schedules dict.
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
        self.__schedules.clear()

    # Function that retrieves every available bus route.
    def get_bus_routes(self):
        response = requests.get(
            'https://api.um.warszawa.pl/api/action/public_transport_routes/?apikey=' + self.__api_key)
        for bus_nr in response.json()['result']:
            for route_type in response.json()['result'][bus_nr]:
                # Bus routes entries are numbered, but they usually aren't sorted by those numbers,
                # so below I'm looking for the biggest number, then I'm creating a list of that length,
                # and then I'm doing a sort of bucket sort (20th element gets assigned to the
                # 20th position in the list)
                max_nr = 0
                for nr in response.json()['result'][bus_nr][route_type]:
                    if int(nr) > max_nr:
                        max_nr = int(nr)
                if bus_nr not in self.__bus_routes:
                    self.__bus_routes[bus_nr] = {}
                self.__bus_routes[bus_nr][route_type] = {}
                self.__bus_routes[bus_nr][route_type] = [None] * max_nr
                for nr in response.json()['result'][bus_nr][route_type]:
                    helper = response.json()['result'][bus_nr][route_type][nr]
                    self.__bus_routes[bus_nr][route_type][int(nr) - 1] = (
                        BusRouteEntry(bus_nr, route_type, helper['ulica_id'], helper['nr_zespolu'],
                                      helper['typ'], helper['nr_przystanku']))

    # Function that dumps bus routes into the given file. This operation clears all data in the __bus_routes dict.
    def dump_bus_routes(self, file_to_dump):
        data_headers = ['Bus_nr', 'Route_code', 'Street_id', 'Stop_team_nr', 'Stop_type', 'Stop_nr']
        with open(file_to_dump, 'w', newline='', encoding='utf16') as file:
            csv_writer = csv.writer(file)
            csv_writer.writerow(data_headers)
            for bus_nr in self.__bus_routes:
                for route_type in self.__bus_routes[bus_nr]:
                    for index in range(len(self.__bus_routes[bus_nr][route_type])):
                        csv_writer.writerow(self.__bus_routes[bus_nr][route_type][index].to_csv())
        self.__bus_routes.clear()
