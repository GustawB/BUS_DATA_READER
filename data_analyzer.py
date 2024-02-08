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
                    coords2 = (self.bus_data[bus_line][bus][i + 1].latitude, self.bus_data[bus_line][bus][i + 1].longitude)
                    dist = geopy.distance.geodesic(coords1, coords2).m
                    speed = self.calc_average_speed(coords1, coords2, sample_length)
                    print(str(dist) + " " + str(speed))
                    if speed > 50.0:
                        nr_of_overspeeds = nr_of_overspeeds + 1

                if nr_of_overspeeds > 0:
                    nr_of_busses_overspeeding = nr_of_busses_overspeeding + 1

        return nr_of_busses_overspeeding

    def find_all_equal_points_on_route(self, coords1, coords2):
        difference_x = abs(coords1[0] - coords2[0])
        difference_y = abs(coords1[1] - coords2[1])




    def point_with_many_overspeeds(self, sample_length):
        for bus_nr in self.bus_data:
            for vehicle_nr in self.bus_data[bus_nr]:
                for i in range(len(self.bus_data[bus_nr][vehicle_nr]) - 1):
                    coords1 = (self.bus_data[bus_nr][vehicle_nr][i].latitude, self.bus_data[bus_nr][vehicle_nr][i].longitude)
                    coords2 = (self.bus_data[bus_nr][vehicle_nr][i+1].latitude, self.bus_data[bus_nr][vehicle_nr][i+1].longitude)
                    speed = self.calc_average_speed(coords1, coords2, sample_length)
                    if speed > 50.0:

