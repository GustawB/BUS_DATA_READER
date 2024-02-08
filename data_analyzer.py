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

    def calc_nr_of_overspeeding_busses(self, sample_length):
        nr_of_busses_overspeeding = 0
        for bus_line in self.bus_data:
            for bus in self.bus_data[bus_line]:
                nr_of_overspeeds = 0
                for i in range(len(self.bus_data[bus_line][bus]) - 1):
                    dist = self.bus_data[bus_line][bus][i + 1].location.distance(self.bus_data[bus_line][bus][i].location)
                    speed = dist / sample_length * 3600 / 1000
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
                    speed = dist / sample_length * 3600 / 1000
                    if speed <= 50:
                        self.points_with_no_overspeeds(self.bus_data[bus_nr][vehicle_nr][i + 1])
                    else:
                        self.points_with_overspeeds(self.bus_data[bus_nr][vehicle_nr][i + 1])

    def calc_overspeed_percentages(self):
        for key in self.points_of_overspeed:
            self.overspeed_percentages[key] = (float(self.points_of_overspeed[key]) /
                                               float(self.nr_of_all_busses_for_ovespeed_points[key]))
