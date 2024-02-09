import csv
from datetime import datetime
import geopy.distance

from data_holders import ZTM_bus, Location, bus_route_entry, bus_stop


class data_analyzer:
    bus_data = dict
    bus_stop_data: dict
    bus_routes_data: dict
    points_of_overspeed: dict
    nr_of_all_busses_for_ovespeed_points: dict
    overspeed_percentages: dict
    times_for_stops: dict
    nr_of_busses_for_stops: dict

    def __init__(self):
        self.bus_data = {}
        self.bus_stop_data = {}
        self.bus_routes_data = {}
        self.points_of_overspeed = {}
        self.nr_of_all_busses_for_ovespeed_points = {}
        self.overspeed_percentages = {}
        self.times_for_stops = {}
        self.nr_of_busses_for_stops = {}

    def read_bus_data(self, bus_filename):
        with open(bus_filename, 'r', encoding='utf16') as file:
            reader = csv.reader(file)
            nr_of_lines = 0
            for row in reader:
                nr_of_lines = nr_of_lines + 1
                if nr_of_lines > 1:
                    bus = ZTM_bus(row[0], float(row[1]), float(row[2]), row[4], row[5],
                                  datetime.strptime(row[6], "%Y-%m-%d %H:%M:%S"), row[3])
                    if row[0] in self.bus_data:
                        if row[4] in self.bus_data[row[0]]:
                            self.bus_data[row[0]][row[4]].append(bus)
                        else:
                            self.bus_data[row[0]][row[4]] = [bus]
                    else:
                        self.bus_data[row[0]] = {row[4]: [bus]}

    def read_bus_stop_data(self, bus_stop_filename):
        with open(bus_stop_filename, 'r', encoding='utf16') as file:
            reader = csv.reader(file)
            nr_of_lines = 0
            for row in reader:
                nr_of_lines += 1
                if nr_of_lines > 1:
                    bs = bus_stop(row[0], row[1], row[2], row[3], row[4], float(row[5]), float(row[6]))
                    if bs.street_id not in self.bus_stop_data:
                        self.bus_stop_data[bs.street_id] = {}
                    if bs.post not in self.bus_stop_data[bs.street_id]:
                        self.bus_stop_data[bs.street_id][bs.post] = []
                    self.bus_stop_data[bs.street_id][bs.post].append(bs)

    def read_bus_routes_data(self, bus_routes_filename):
        with open(bus_routes_filename, 'r', encoding='utf16') as file:
            reader = csv.reader(file)
            nr_of_lines = 0
            for row in reader:
                nr_of_lines += 1
                if nr_of_lines > 1:
                    bre = bus_route_entry(row[0], row[1], row[2], row[3], row[4], row[5])
                    if row[0] not in self.bus_routes_data:
                        self.bus_routes_data[row[0]] = {}
                    if row[1] not in self.bus_routes_data[row[0]]:
                        self.bus_routes_data[row[0]][row[1]] = []
                    self.bus_routes_data[row[0]][row[1]].append(bre)



    def normalise_avg_speed(self, sample_length, dist):
        local_length = sample_length
        speed = dist / local_length * 3600 / 1000
        while speed > 100:
            local_length += 1
            speed = dist / local_length * 3600 / 1000
        return speed

    def calc_nr_of_overspeeding_busses(self, sample_length):
        nr_of_busses_overspeeding = 0
        for bus_line in self.bus_data:
            for bus in self.bus_data[bus_line]:
                nr_of_overspeeds = 0
                for i in range(len(self.bus_data[bus_line][bus]) - 1):
                    dist = self.bus_data[bus_line][bus][i + 1].location.distance(self.bus_data[bus_line][bus][i].location)
                    speed = self.normalise_avg_speed(sample_length, dist)
                    print(speed)
                    if speed > 50.0:
                        nr_of_overspeeds = nr_of_overspeeds + 1

                if nr_of_overspeeds > 0:
                    nr_of_busses_overspeeding = nr_of_busses_overspeeding + 1

        return nr_of_busses_overspeeding

    def points_with_no_overspeeds(self, bus):
        if bus.location.street_name in self.nr_of_all_busses_for_ovespeed_points:
            self.nr_of_all_busses_for_ovespeed_points[bus.location.street_name] += 1
        else:
            self.nr_of_all_busses_for_ovespeed_points[bus.location.street_name] = 1

    def points_with_overspeeds(self, bus):
        if bus.location.street_name in self.points_of_overspeed:
            self.points_of_overspeed[bus.location.street_name] += 1
        else:
            self.points_of_overspeed[bus.location.street_name] = 1

        self.points_with_no_overspeeds(bus)


    def calc_data_for_overspeed_percentages(self, sample_length):
        number = 0
        for bus_nr in self.bus_data:
            for vehicle_nr in self.bus_data[bus_nr]:
                number += 1
                for i in range(len(self.bus_data[bus_nr][vehicle_nr]) - 1):
                    dist = self.bus_data[bus_nr][vehicle_nr][i + 1].location.distance(
                        self.bus_data[bus_nr][vehicle_nr][i].location)
                    speed = self.normalise_avg_speed(sample_length, dist)
                    if speed <= 50:
                        self.points_with_no_overspeeds(self.bus_data[bus_nr][vehicle_nr][i + 1])
                    else:
                        self.points_with_overspeeds(self.bus_data[bus_nr][vehicle_nr][i + 1])

    def calc_overspeed_percentages(self):
        for key in self.points_of_overspeed:
            self.overspeed_percentages[key] = (float(self.points_of_overspeed[key]) /
                                               float(self.nr_of_all_busses_for_ovespeed_points[key]))

    def calc_time_difference(self, bus, bs_data, route_code):
        min_diff
        with open('schedules/' + bs_data.team + '_' + bs_data.post + '_' + bus.line) as file:
            csv_reader = csv.reader(file)
            for row in csv_reader:
                if row[2] == route_code:


    def bus_stops_in_one_sample(self, loc_a, loc_b, bus):
        diff_x = loc_b.longitude - loc_a.longitude
        diff_y = loc_b.latitude - loc_a.latitude
        diff_x /= 8
        diff_y /= 8
        loc_c = Location(loc_a.longitude, loc_a.latitude)

        for i in range(9):
            for route_code in self.bus_routes_data[bus.line]:
                for bre in self.bus_routes_data[bus.line][route_code]:
                    for bs_data in self.bus_stop_data[bre.street_id][bre.bus_stop_nr]:
                        if loc_c == bs_data.data.location:








    def calc_times_for_stops(self):
        for bus_nr in self.bus_data:
            for vehicle_nr in self.bus_data[bus_nr]:
                for i in range(len(self.bus_data[bus_nr][vehicle_nr]) - 1):
                    self.bus_stops_in_one_sample(self.bus_data[bus_nr][vehicle_nr][i].location,
                                                 self.bus_data[bus_nr][vehicle_nr][i + 1].location)

