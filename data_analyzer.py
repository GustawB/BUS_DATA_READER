import csv
import datetime
import datetime as dt
import os.path

import geopy.distance

from data_holders import ZTM_bus, Location, bus_route_entry, bus_stop, bus_schedule_entry


class data_analyzer:
    bus_data = dict
    bus_stop_data: dict
    bus_routes_data: dict
    points_of_overspeed: dict
    nr_of_all_busses_for_ovespeed_points: dict
    overspeed_percentages: dict
    times_for_stops: dict
    nr_of_busses_for_stops: dict
    avg_times_for_stops: dict

    def __init__(self):
        self.bus_data = {}
        self.bus_stop_data = {}
        self.bus_routes_data = {}
        self.points_of_overspeed = {}
        self.nr_of_all_busses_for_ovespeed_points = {}
        self.overspeed_percentages = {}
        self.times_for_stops = {}
        self.nr_of_busses_for_stops = {}
        self.avg_times_for_stops = {}

    def read_bus_data(self, bus_filename):
        with open(bus_filename, 'r', encoding='utf16') as file:
            reader = csv.reader(file)
            nr_of_lines = 0
            for row in reader:
                nr_of_lines = nr_of_lines + 1
                if nr_of_lines > 1:
                    bus = ZTM_bus(row[0], float(row[1]), float(row[2]), row[4], row[5],
                                  dt.datetime.strptime(row[6], "%Y-%m-%d %H:%M:%S"), row[3])
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
                    dist = self.bus_data[bus_line][bus][i + 1].location.distance(
                        self.bus_data[bus_line][bus][i].location)
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
        min_diff = 100000
        filename = 'schedules/' + bs_data.team + '_' + bs_data.post + '_' + bus.line + '.csv'
        if not os.path.isfile(filename):
            return None
        with open(filename, 'r', encoding='utf16') as file:
            csv_reader = csv.reader(file)
            for row in csv_reader:
                # print(row)
                if row[2] == route_code:
                    time_data = dt.datetime.strptime(row[3], "%Y-%m-%d %H:%M:%S")
                    # print(type(bus.time_data))
                    time_data_new = datetime.datetime(bus.time_data.year, bus.time_data.month, bus.time_data.day,
                                                      time_data.hour, time_data.minute, time_data.second)

                    difference = bus.time_data - time_data_new
                    #print(str(bus.time_data) + ' ' + str(time_data_new))
                    if abs(difference.total_seconds()) < abs(min_diff):
                        min_diff = difference.total_seconds()
        #print(min_diff)
        return min_diff

    def bus_stops_in_one_sample(self, loc_a, loc_b, bus):
        diff_x = loc_b.longitude - loc_a.longitude
        diff_y = loc_b.latitude - loc_a.latitude
        diff_x /= 8
        diff_y /= 8
        loc_c = Location(loc_a.longitude, loc_a.latitude)
        found_bus_stops = {}
        for i in range(9):
            for route_code in self.bus_routes_data[bus.line]:
                for bre in self.bus_routes_data[bus.line][route_code]:
                    for bs_data in self.bus_stop_data[bre.street_id][bre.bus_stop_nr]:
                        if loc_c == bs_data.location:
                            delay = self.calc_time_difference(bus, bs_data, route_code)
                            if delay is not None and bs_data in found_bus_stops:
                                temp = found_bus_stops[bs_data]
                                found_bus_stops[bs_data] = min(delay, temp)
                                #print(found_bus_stops[bs_data])
                            elif delay is not None:
                                found_bus_stops[bs_data] = delay
            loc_c.longitude += diff_x
            loc_c.latitude += diff_y

        return found_bus_stops

    def calc_times_for_stops(self):
        for bus_nr in self.bus_data:
            for vehicle_nr in self.bus_data[bus_nr]:
                for i in range(len(self.bus_data[bus_nr][vehicle_nr]) - 1):
                    found_bus_stops = self.bus_stops_in_one_sample(self.bus_data[bus_nr][vehicle_nr][i].location,
                                                                   self.bus_data[bus_nr][vehicle_nr][i + 1].location,
                                                                   self.bus_data[bus_nr][vehicle_nr][i + 1])
                    for key in found_bus_stops:
                        if key in self.times_for_stops:
                            self.times_for_stops[key] += found_bus_stops[key]
                            self.nr_of_busses_for_stops[key] += 1
                        else:
                            self.times_for_stops[key] = found_bus_stops[key]
                            self.nr_of_busses_for_stops[key] = 1

    def calc_average_delays(self):
        for key in self.nr_of_busses_for_stops:
            new_key = key.team_name + '_' + key.post
            self.avg_times_for_stops[new_key] = (float(self.times_for_stops[key]) /
                                                 float(self.nr_of_busses_for_stops[key]))
