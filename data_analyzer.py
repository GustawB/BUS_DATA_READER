import csv
import datetime
import datetime as dt
import os.path

from data_holders import ZTMBus, Location, BusRouteEntry, BusStop, BusScheduleEntry


class DataAnalyzer:
    bus_data = dict
    bus_stop_data: dict
    bus_routes_data: dict
    points_of_overspeed: dict
    nr_of_all_busses_for_ovespeed_points: dict
    overspeed_percentages: dict
    times_for_stops: dict
    nr_of_busses_for_stops: dict
    avg_times_for_stops: dict
    schedules: dict

    nr_of_invalid_speeds: int
    nr_of_invalid_times: int
    nr_of_non_existing_schedules: int
    nr_of_unread_buses: int

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
        self.schedules = {}

        self.nr_of_invalid_speeds = 0
        self.nr_of_invalid_times = 0
        self.nr_of_non_existing_schedules = 0
        self.nr_of_unread_buses = 0

    def read_schedules_data(self, dir_with_schedules, dir_length):
        with os.scandir(dir_with_schedules) as it:
            for entry in it:
                team = entry.path[dir_length + 1:dir_length + 5]
                post = entry.path[dir_length + 6:dir_length + 8]
                bus = entry.path[dir_length + 9:dir_length + 12]
                if team not in self.schedules:
                    self.schedules[team] = {}
                if post not in self.schedules[team]:
                    self.schedules[team][post] = {}
                if bus not in self.schedules[team][post]:
                    self.schedules[team][post][bus] = []
                with open(entry.path, 'r', encoding='utf16') as file:
                    csv_reader = csv.reader(file)
                    nr_of_lines = 0
                    for row in csv_reader:
                        if nr_of_lines > 0:
                            self.schedules[team][post][bus].append(row)
                        nr_of_lines += 1

    def read_bus_data(self, bus_filename):
        with open(bus_filename, 'r', encoding='utf16') as file:
            reader = csv.reader(file)
            nr_of_lines = 0
            for row in reader:
                nr_of_lines = nr_of_lines + 1
                if nr_of_lines > 1:
                    street_name = row[3]
                    if street_name[:5] == 'ulica':
                        street_name = street_name[6:]
                    bus = ZTMBus(row[0], float(row[1]), float(row[2]), row[4], row[5], row[6], False, street_name)
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
                    bs = BusStop(row[0], row[1], row[2], row[3], row[4], float(row[5]), float(row[6]))
                    if bs.team not in self.bus_stop_data:
                        self.bus_stop_data[bs.team] = {}
                    self.bus_stop_data[bs.team][bs.post] = bs

    def read_bus_routes_data(self, bus_routes_filename):
        with open(bus_routes_filename, 'r', encoding='utf16') as file:
            reader = csv.reader(file)
            nr_of_lines = 0
            for row in reader:
                nr_of_lines += 1
                if nr_of_lines > 1:
                    bre = BusRouteEntry(row[0], row[1], row[2], row[3], row[4], row[5])
                    if row[0] not in self.bus_routes_data:
                        self.bus_routes_data[row[0]] = {}
                    if row[1] not in self.bus_routes_data[row[0]]:
                        self.bus_routes_data[row[0]][row[1]] = []
                    self.bus_routes_data[row[0]][row[1]].append(bre)

    def normalise_avg_speed(self, dist, prev_bus, next_bus):
        local_length = next_bus.time_data - prev_bus.time_data
        # print(local_length)
        if local_length <= 0:
            # print(str(prev_bus.time_data) + ' ' + str(next_bus.time_data))
            self.nr_of_invalid_times += 1
            return -1
        speed = dist / local_length * 3600 / 1000
        if speed >= 120 or speed <= 0:
            self.nr_of_invalid_speeds += 1
            return -1
        return speed

    def calc_nr_of_overspeeding_busses(self):
        self.nr_of_invalid_times = 0
        nr_of_busses_overspeeding = 0
        for bus_line in self.bus_data:
            for bus in self.bus_data[bus_line]:
                nr_of_overspeeds = 0
                for i in range(len(self.bus_data[bus_line][bus]) - 1):
                    dist = self.bus_data[bus_line][bus][i + 1].location.distance(
                        self.bus_data[bus_line][bus][i].location)
                    speed = self.normalise_avg_speed(dist, self.bus_data[bus_line][bus][i],
                                                     self.bus_data[bus_line][bus][i + 1])
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

    def calc_data_for_overspeed_percentages(self):
        self.nr_of_invalid_times = 0
        iterator = 0
        print(len(self.bus_data))
        for bus_nr in self.bus_data:
            iterator += 1
            print(iterator)
            for vehicle_nr in self.bus_data[bus_nr]:
                for i in range(len(self.bus_data[bus_nr][vehicle_nr]) - 1):
                    dist = self.bus_data[bus_nr][vehicle_nr][i + 1].location.distance(
                        self.bus_data[bus_nr][vehicle_nr][i].location)
                    speed = self.normalise_avg_speed(dist, self.bus_data[bus_nr][vehicle_nr][i],
                                                     self.bus_data[bus_nr][vehicle_nr][i + 1])
                    if 50 >= speed >= 0:
                        self.points_with_no_overspeeds(self.bus_data[bus_nr][vehicle_nr][i + 1])
                    elif speed > 50:
                        self.points_with_overspeeds(self.bus_data[bus_nr][vehicle_nr][i + 1])

    def calc_overspeed_percentages(self, file_to_dump):
        for key in self.points_of_overspeed:
            self.overspeed_percentages[key] = (float(self.points_of_overspeed[key]) /
                                               float(self.nr_of_all_busses_for_ovespeed_points[key]))
        data_headers = ['Street_name', 'Percentage']
        with open(file_to_dump, 'w', newline='', encoding='utf16') as file:
            csv_writer = csv.writer(file)
            csv_writer.writerow(data_headers)
            for data in sorted(self.overspeed_percentages, key=self.overspeed_percentages.get, reverse=True):
                data_list = [data, str(int(self.overspeed_percentages[data] * 100))]
                csv_writer.writerow(data_list)

    def calc_time_difference(self, bus_line, bus_time, bs_data, route_code):
        min_diff = 100000
        #print(str(bs_data.team) + ' ' + str(bs_data.post) + ' ' + str(bus.line))
        try:
            for row in self.schedules[bs_data.team][bs_data.post][bus_line]:
                if row[2] == route_code:
                    time_sec = int(row[3])
                    difference = bus_time - time_sec
                    if abs(difference) < abs(min_diff):
                        min_diff = difference
        except KeyError:
            self.nr_of_non_existing_schedules += 1
            return None
        except ValueError:
            return None
        return min_diff

    def bus_stops_in_one_sample(self, prev_bus, next_bus):
        diff_x = next_bus.location.longitude - prev_bus.location.longitude
        diff_y = next_bus.location.latitude - prev_bus.location.latitude
        time_diff = next_bus.time_data - prev_bus.time_data
        diff_x /= 8
        diff_y /= 8
        time_diff /= 8
        loc_c = next_bus.location
        local_time_data = prev_bus.time_data
        found_bus_stops = {}
        for i in range(9):
            if next_bus.line not in self.bus_routes_data:
                self.nr_of_unread_buses += 1
                break
            for route_code in self.bus_routes_data[next_bus.line]:
                for bre in self.bus_routes_data[next_bus.line][route_code]:
                    if next_bus.line[0] != 'Z':
                        bs_data = self.bus_stop_data[bre.team_nr][bre.bus_stop_nr]
                        if loc_c == bs_data.location:
                            delay = self.calc_time_difference(next_bus.line, local_time_data, bs_data, route_code)
                            if delay is not None and delay != 100000 and bs_data in found_bus_stops:
                                #print(str(next_bus.line) + ' ' + str(bre.team_nr) + ' ' + str(
                                 #   bre.bus_stop_nr) + ' ' + str(
                                  #  route_code) + ' ' + str(delay))
                                temp = found_bus_stops[bs_data]
                                found_bus_stops[bs_data] = min(abs(delay), abs(temp))
                                # print(found_bus_stops[bs_data])
                            elif delay is not None and delay != 100000:
                                #print(delay)
                                found_bus_stops[bs_data] = delay
            loc_c.longitude(loc_c.longitude + diff_x)
            loc_c.latitude(loc_c.latitude + diff_y)
            local_time_data += time_diff

        return found_bus_stops

    def calc_times_for_stops(self):
        print(len(self.bus_data))
        nr = 0
        for bus_nr in self.bus_data:
            print(nr)
            nr += 1
            for vehicle_nr in self.bus_data[bus_nr]:
                # print(len(self.bus_data[bus_nr][vehicle_nr]))
                for i in range(len(self.bus_data[bus_nr][vehicle_nr]) - 1):
                    found_bus_stops = self.bus_stops_in_one_sample(self.bus_data[bus_nr][vehicle_nr][i],
                                                                   self.bus_data[bus_nr][vehicle_nr][i + 1])
                    for key in found_bus_stops:
                        if key in self.times_for_stops:
                            self.times_for_stops[key] += found_bus_stops[key]
                            self.nr_of_busses_for_stops[key] += 1
                        else:
                            self.times_for_stops[key] = found_bus_stops[key]
                            self.nr_of_busses_for_stops[key] = 1

    def calc_average_delays(self, file_to_dump, upper_limit, lower_limit):
        for key in self.nr_of_busses_for_stops:
            new_key = key.team_name + '_' + key.post
            self.avg_times_for_stops[new_key] = (float(self.times_for_stops[key]) /
                                                 float(self.nr_of_busses_for_stops[key]))

        with open(file_to_dump, 'w', newline='', encoding='utf16') as file:
            data_headers = ['Bus_stop', 'Avg_time']
            csv_writer = csv.writer(file)
            csv_writer.writerow(data_headers)
            for data in sorted(self.avg_times_for_stops, key=self.avg_times_for_stops.get, reverse=True):
                if upper_limit > self.avg_times_for_stops[data] > lower_limit:
                    data_list = [data, str(self.avg_times_for_stops[data])]
                    csv_writer.writerow(data_list)

    def dump_invalid_data_stats(self, file_to_dump):
        data_headers = ['Error_type', 'nr_of_entries']
        with open(file_to_dump, 'w', newline='', encoding='utf16') as file:
            csv_writer = csv.writer(file)
            csv_writer.writerow(data_headers)
            data_list = ['invalid_speeds', str(self.nr_of_invalid_speeds)]
            csv_writer.writerow(data_list)
            data_list = ['invalid_times', str(self.nr_of_invalid_times)]
            csv_writer.writerow(data_list)
            data_list = ['non_existing_schedules', str(self.nr_of_non_existing_schedules)]
            csv_writer.writerow(data_list)


        
