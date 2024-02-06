import csv
from datetime import datetime
import geopy.distance

from data_holders import ZTM_bus


class data_analyzer:
    bus_data = dict

    def __init__(self):
        self.bus_data = {}

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

    def calc_nr_of_overspeeding_busses(self, sample_length):
        nr_of_busses_overspeeding = 0
        for bus_line in self.bus_data:
            for bus in self.bus_data[bus_line]:
                nr_of_overspeeds = 0
                for i in range(len(self.bus_data[bus_line][bus]) - 1):
                    coords1 = (self.bus_data[bus_line][bus][i].latitude, self.bus_data[bus_line][bus][i].longitude)
                    coords2 = (self.bus_data[bus_line][bus][i + 1].latitude, self.bus_data[bus_line][bus][i + 1].longitude)
                    dist = geopy.distance.geodesic(coords1, coords2).m
                    speed = dist / sample_length * 3600 / 1000
                    print(str(dist) + " " + str(speed))
                    if speed > 50.0:
                        nr_of_overspeeds = nr_of_overspeeds + 1

                if nr_of_overspeeds > 0:
                    nr_of_busses_overspeeding = nr_of_busses_overspeeding + 1

        return nr_of_busses_overspeeding
