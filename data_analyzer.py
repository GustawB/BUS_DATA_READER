import csv
from datetime import datetime
import geopy.distance

from data_holders import ZTM_bus, Location


class data_analyzer:
    bus_data = dict
    points_of_overspeed: dict
    nr_of_all_busses_for_ovespeed_points: dict
    overspeed_percentages: dict

    def __init__(self):
        self.bus_data = {}
        self.points_of_overspeed = {}
        self.nr_of_all_busses_for_ovespeed_points = {}
        self.overspeed_percentages = {}

    def read_bus_data(self, bus_filename):
        with open(bus_filename, 'r') as file:
            reader = csv.reader(file)
            nr_of_lines = 0
            for row in reader:
                nr_of_lines = nr_of_lines + 1
                if nr_of_lines > 1:
                    bus = ZTM_bus(row[0], row[1], row[2], row[3], row[4],
                                  datetime.strptime(row[5], "%Y-%m-%d %H:%M:%S"))
                    if row[0] in self.bus_data:
                        if row[3] in self.bus_data[row[0]]:
                            self.bus_data[row[0]][row[3]].append(bus)
                        else:
                            self.bus_data[row[0]][row[3]] = [bus]
                    else:
                        self.bus_data[row[0]] = {row[3]: [bus]}

    def calc_average_speed(self, coords1, coords2, sample_length):
        dist = geopy.distance.geodesic(coords1, coords2).m
        speed = dist / sample_length * 3600 / 1000
        return speed

    def calc_nr_of_overspeeding_busses(self, sample_length):
        nr_of_busses_overspeeding = 0
        for bus_line in self.bus_data:
            for bus in self.bus_data[bus_line]:
                nr_of_overspeeds = 0
                for i in range(len(self.bus_data[bus_line][bus]) - 1):
                    coords1 = (self.bus_data[bus_line][bus][i].latitude, self.bus_data[bus_line][bus][i].longitude)
                    coords2 = (
                        self.bus_data[bus_line][bus][i + 1].latitude, self.bus_data[bus_line][bus][i + 1].longitude)
                    dist = geopy.distance.geodesic(coords1, coords2).m
                    speed = self.calc_average_speed(coords1, coords2, sample_length)
                    print(str(dist) + " " + str(speed))
                    if speed > 50.0:
                        nr_of_overspeeds = nr_of_overspeeds + 1

                if nr_of_overspeeds > 0:
                    nr_of_busses_overspeeding = nr_of_busses_overspeeding + 1

        return nr_of_busses_overspeeding

    def points_with_overspeeds(self, coords1, coords2):
        difference_x = coords2[0] - coords1[0]
        difference_y = coords2[1] - coords1[1]
        difference_x = difference_x / 8
        difference_y = difference_y / 8
        used_keys = []
        coords3 = coords1
        for i in range(9):
            local_used_keys_nr = 0
            location = Location(coords3[0], coords3[1])
            for key in self.points_of_overspeed:
                if location == key and key not in used_keys:
                    local_used_keys_nr += 1
                    used_keys.append(key)
                    current1 = self.points_of_overspeed[key]
                    current2 = self.nr_of_all_busses_for_ovespeed_points[key]
                    self.points_of_overspeed[key] = current1 + 1
                    self.nr_of_all_busses_for_ovespeed_points[key] = current2 + 1
            if local_used_keys_nr == 0 and location not in used_keys:
                used_keys.append(location)
                self.points_of_overspeed[location] = 1
                self.nr_of_all_busses_for_ovespeed_points[location] = 1

            coords3 = (coords3[0] + difference_x, coords3[1] + difference_y)

    def points_with_no_overspeeds(self, coords1, coords2):
        difference_x = coords2[0] - coords1[0]
        difference_y = coords2[1] - coords1[1]
        difference_x = difference_x / 8
        difference_y = difference_y / 8
        used_keys = []
        coords3 = coords1
        for i in range(9):
            location = Location(coords3[0], coords3[1])
            local_used_keys_nr = 0
            for key in self.nr_of_all_busses_for_ovespeed_points:
                if location == key and key not in used_keys:
                    local_used_keys_nr += 1
                    used_keys.append(key)
                    current = self.nr_of_all_busses_for_ovespeed_points[key]
                    self.nr_of_all_busses_for_ovespeed_points[key] = current + 1
            if local_used_keys_nr == 0 and location not in used_keys:
                used_keys.append(location)
                self.nr_of_all_busses_for_ovespeed_points[location] = 1
                self.points_of_overspeed[location] = 0

            coords3 = (coords3[0] + difference_x, coords3[1] + difference_y)

    def calc_data_for_overspeed_percentages(self, sample_length):
        for bus_nr in self.bus_data:
            for vehicle_nr in self.bus_data[bus_nr]:
                for i in range(len(self.bus_data[bus_nr][vehicle_nr]) - 1):
                    coords1 = (
                        self.bus_data[bus_nr][vehicle_nr][i].latitude, self.bus_data[bus_nr][vehicle_nr][i].longitude)
                    coords2 = (self.bus_data[bus_nr][vehicle_nr][i + 1].latitude,
                               self.bus_data[bus_nr][vehicle_nr][i + 1].longitude)
                    speed = self.calc_average_speed(coords1, coords2, sample_length)
                    if speed <= 50:
                        self.points_with_no_overspeeds(coords1, coords2)
                    else:
                        self.points_with_overspeeds(coords1, coords2)

    def calc_overspeed_percentages(self):
        for key in self.points_of_overspeed:
            self.overspeed_percentages[key] = (float(self.points_of_overspeed[key]) /
                                               float(self.nr_of_all_busses_for_ovespeed_points[key]))
