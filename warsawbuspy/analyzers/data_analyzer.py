import csv
import json
import os.path

from warsawbuspy.holders.data_holders import ZTMBus, BusRouteEntry, BusStop
from warsawbuspy.utility.data_utility import assert_file_extension


# Class responsible for analyzing the data collected by the DataReader class.
class DataAnalyzer:
    __slots__ = ('__bus_data', '__bus_stop_data', '__bus_routes_data', '__points_of_overspeed',
                 '__nr_of_all_busses_for_ovespeed_points', '__overspeed_percentages', '__times_for_stops',
                 '__nr_of_buses_for_stops', '__avg_times_for_stops', '__schedules', '__overspeeds_json',
                 '__nr_of_invalid_speeds', '__nr_of_invalid_times', '__nr_of_unread_buses', '__unread_stops')

    def __init__(self):
        self.__bus_data = {}
        self.__bus_stop_data = {}
        self.__bus_routes_data = {}
        self.__points_of_overspeed = {}
        self.__nr_of_all_busses_for_ovespeed_points = {}
        self.__overspeed_percentages = {}
        self.__times_for_stops = {}
        self.__nr_of_buses_for_stops = {}
        self.__avg_times_for_stops = {}
        self.__schedules = {}
        self.__unread_stops = {}
        self.__overspeeds_json = {
            "type": "FeatureCollection",
            "features": []}

        self.__nr_of_invalid_speeds = 0
        self.__nr_of_invalid_times = 0
        self.__nr_of_unread_buses = 0

    @property
    def bus_data(self) -> dict:
        return self.__bus_data

    @property
    def bus_stop_data(self) -> dict:
        return self.__bus_stop_data

    @property
    def bus_routes_data(self) -> dict:
        return self.__bus_routes_data

    @property
    def points_of_overspeed(self) -> dict:
        return self.__points_of_overspeed

    @property
    def nr_of_all_busses_for_ovespeed_points(self) -> dict:
        return self.__nr_of_all_busses_for_ovespeed_points

    @property
    def overspeed_percentages(self) -> dict:
        return self.__overspeed_percentages

    @property
    def times_for_stops(self) -> dict:
        return self.__times_for_stops

    @property
    def nr_of_buses_for_stops(self) -> dict:
        return self.__nr_of_buses_for_stops

    @property
    def avg_times_for_stops(self) -> dict:
        return self.__avg_times_for_stops

    @property
    def schedules(self) -> dict:
        return self.__schedules

    @property
    def nr_of_invalid_speeds(self) -> int:
        return self.__nr_of_invalid_speeds

    @property
    def nr_of_invalid_times(self) -> int:
        return self.__nr_of_invalid_times

    @property
    def nr_of_unread_buses(self) -> int:
        return self.__nr_of_unread_buses

    @property
    def overspeeds_json(self) -> dict:
        return self.__overspeeds_json

    # Function that reads the bus schedules data from the given directory.
    def read_schedules_data(self, dir_with_schedules: str) -> None:
        dir_length = len(dir_with_schedules)
        with os.scandir(dir_with_schedules) as it:
            for entry in it:
                # Extracting bus team, bus post and bus nr from the file name.
                team = entry.path[dir_length + 1:dir_length + 5]
                post = entry.path[dir_length + 6:dir_length + 8]
                bus = entry.path[dir_length + 9:dir_length + 12]
                if team not in self.__schedules:
                    self.__schedules[team] = {}
                if post not in self.__schedules[team]:
                    self.__schedules[team][post] = {}
                if bus not in self.__schedules[team][post]:
                    self.__schedules[team][post][bus] = []
                with open(entry.path, 'r', encoding='utf16') as file:
                    csv_reader = csv.reader(file)
                    nr_of_lines = 0
                    for row in csv_reader:
                        if nr_of_lines > 0:
                            self.__schedules[team][post][bus].append(row)
                        nr_of_lines += 1

    # Function that reads the bus data from the given file.
    def read_bus_data(self, bus_filename: str) -> None:
        assert_file_extension(bus_filename, '.csv')
        with open(bus_filename, 'r', encoding='utf16') as file:
            reader = csv.reader(file)
            nr_of_lines = 0
            for row in reader:
                nr_of_lines = nr_of_lines + 1
                if nr_of_lines > 1:
                    street_name = row[3]
                    # Cutting the unnecessary part of the street name.
                    street_name.replace('ulica', '')
                    bus = ZTMBus(row[0], float(row[1]), float(row[2]), row[4], row[5], row[6], False, street_name)
                    if row[0] in self.__bus_data:
                        if row[4] in self.__bus_data[row[0]]:
                            self.__bus_data[row[0]][row[4]].append(bus)
                        else:
                            self.__bus_data[row[0]][row[4]] = [bus]
                    else:
                        self.__bus_data[row[0]] = {row[4]: [bus]}

    # Function that reads the bus stop data from the given file.
    def read_bus_stop_data(self, bus_stop_filename: str) -> None:
        assert_file_extension(bus_stop_filename, '.csv')
        with open(bus_stop_filename, 'r', encoding='utf16') as file:
            reader = csv.reader(file)
            nr_of_lines = 0
            for row in reader:
                nr_of_lines += 1
                if nr_of_lines > 1:
                    bs = BusStop(row[0], row[1], row[2], row[3], row[4], float(row[5]), float(row[6]))
                    if bs.team not in self.__bus_stop_data:
                        self.__bus_stop_data[bs.team] = {}
                    self.__bus_stop_data[bs.team][bs.post] = bs

    # Function that reads the bus routes data from the given file.
    def read_bus_routes_data(self, bus_routes_filename: str) -> None:
        assert_file_extension(bus_routes_filename, '.csv')
        with open(bus_routes_filename, 'r', encoding='utf16') as file:
            reader = csv.reader(file)
            nr_of_lines = 0
            for row in reader:
                nr_of_lines += 1
                if nr_of_lines > 1:
                    bre = BusRouteEntry(row[0], row[1], row[2], row[3], row[4], row[5])
                    if row[0] not in self.__bus_routes_data:
                        self.__bus_routes_data[row[0]] = {}
                    if row[1] not in self.__bus_routes_data[row[0]]:
                        self.__bus_routes_data[row[0]][row[1]] = []
                    self.__bus_routes_data[row[0]][row[1]].append(bre)

    # Function that checks if the speed of a bus is valid (is not negative or isn't greater than 120 km/h,
    # because buses shouldn't be able to reach speed like that in the city area). Also, it checks if the bus
    # didn't send the same information twice by comparing the times of sending the info.
    def __normalise_avg_speed(self, dist: float, prev_bus: ZTMBus, next_bus: ZTMBus) -> float:
        local_length = next_bus.time_data - prev_bus.time_data
        if local_length <= 0:
            self.__nr_of_invalid_times += 1
            return -1
        speed = dist / local_length * 3600 / 1000
        if speed >= 120 or speed < 0:
            self.__nr_of_invalid_speeds += 1
            return -1
        return speed

    # Function that returns the number of busses that were overspeeding at least once
    # during the period of data sampling, and collects every location at which any bus was ovespeeding.
    def calc_nr_of_overspeeding_busses(self) -> int:
        self.__nr_of_invalid_times = 0
        nr_of_busses_overspeeding = 0
        for bus_line in self.__bus_data:
            for bus in self.__bus_data[bus_line]:
                nr_of_overspeeds = 0
                for i in range(len(self.__bus_data[bus_line][bus]) - 1):
                    curr_bus_data = self.__bus_data[bus_line][bus][i]
                    next_bus_data = self.__bus_data[bus_line][bus][i + 1]
                    dist = next_bus_data.location.distance(curr_bus_data.location)
                    speed = self.__normalise_avg_speed(dist, curr_bus_data, next_bus_data)
                    if speed > 50.0:
                        nr_of_overspeeds = nr_of_overspeeds + 1
                        self.__overspeeds_json['features'].append({
                            "type": "Feature",
                            "geometry": {
                                "type": "Point",
                                "coordinates":
                                    [
                                        next_bus_data.location.longitude,
                                        next_bus_data.location.latitude
                                    ]
                            }
                        })
                if nr_of_overspeeds > 0:
                    nr_of_busses_overspeeding = nr_of_busses_overspeeding + 1
        return nr_of_busses_overspeeding

    # Function that dumps the locations of the overspeeds into the given .geojson file.
    # This operation clears the data in __overspeed_json.
    def dump_overspeed_locations(self, file_to_dump_locations: str) -> None:
        assert_file_extension(file_to_dump_locations, '.geojson')
        with open(file_to_dump_locations, 'w') as geojson_file:
            data_to_dump = json.dumps(self.__overspeeds_json, indent=4)
            geojson_file.write(data_to_dump)
        self.__overspeeds_json.clear()

    # Utility function that updates variables related to the number of tested locations.
    def __points_with_no_overspeeds(self, bus: ZTMBus) -> None:
        if bus.location.street_name in self.__nr_of_all_busses_for_ovespeed_points:
            self.__nr_of_all_busses_for_ovespeed_points[bus.location.street_name] += 1
        else:
            self.__nr_of_all_busses_for_ovespeed_points[bus.location.street_name] = 1

    # Utility function that updates variables related to the nr of all tested locations as well as those
    # which are points where buses are ovespeeding.
    def __points_with_overspeeds(self, bus: ZTMBus) -> None:
        if bus.location.street_name in self.__points_of_overspeed:
            self.__points_of_overspeed[bus.location.street_name] += 1
        else:
            self.__points_of_overspeed[bus.location.street_name] = 1
        self.__points_with_no_overspeeds(bus)

    # Function that finds every street for which at least one bus was overspeeding,
    # and then for each one of them it finds the nr of those buses, as well as the nr of
    # all buses that were going through it.
    def __calc_data_for_overspeed_percentages(self) -> None:
        self.__nr_of_invalid_times = 0
        for bus_nr in self.__bus_data:
            for vehicle_nr in self.__bus_data[bus_nr]:
                for i in range(len(self.__bus_data[bus_nr][vehicle_nr]) - 1):
                    dist = self.__bus_data[bus_nr][vehicle_nr][i + 1].location.distance(
                        self.__bus_data[bus_nr][vehicle_nr][i].location)
                    speed = self.__normalise_avg_speed(dist, self.__bus_data[bus_nr][vehicle_nr][i],
                                                       self.__bus_data[bus_nr][vehicle_nr][i + 1])
                    if 50 >= speed >= 0:
                        self.__points_with_no_overspeeds(self.__bus_data[bus_nr][vehicle_nr][i + 1])
                    elif speed > 50:
                        self.__points_with_overspeeds(self.__bus_data[bus_nr][vehicle_nr][i + 1])

    # Function that calculates the percentage of ovespeeding buses for every
    # registered location (location where at least one bus was overspeeding).
    def calc_overspeed_percentages(self) -> None:
        self.__calc_data_for_overspeed_percentages()
        for key in self.__points_of_overspeed:
            self.__overspeed_percentages[key] = (float(self.__points_of_overspeed[key]) /
                                                 float(self.__nr_of_all_busses_for_ovespeed_points[key]))

    # Function that dumps overspeed percentages data into the given .csv file.
    # This operation deletes data in __overspeed_percentages, __points_of_overspeed
    # and __nr_of_all_busses_for_ovespeed_points.
    def dump_overspeed_percentages(self, file_to_dump_percentages: str) -> None:
        assert_file_extension(file_to_dump_percentages, '.csv')
        data_headers = ['Street_name', 'Percentage']
        with open(file_to_dump_percentages, 'w', newline='', encoding='utf16') as file:
            csv_writer = csv.writer(file)
            csv_writer.writerow(data_headers)
            for data in sorted(self.__overspeed_percentages, key=self.__overspeed_percentages.get, reverse=True):
                data_list = [str(data), str(self.__overspeed_percentages[data] * 100)]
                csv_writer.writerow(data_list)
        self.__overspeed_percentages.clear()
        self.__points_of_overspeed.clear()
        self.__nr_of_all_busses_for_ovespeed_points.clear()

    # Function that finds the delay for the given bus on the given stop.
    def __calc_time_difference(self, bus_line: str, bus_brigade: str, bus_time: int,
                               bs_data: BusStop, route_code: str) -> int:
        min_diff = 100000
        try:
            for row in self.__schedules[bs_data.team][bs_data.post][bus_line]:
                if row[2] == route_code and row[0] == bus_brigade:
                    time_sec = int(row[3])
                    difference = bus_time - time_sec
                    # We are always picking the bus stop for which the bus delay was the smallest.
                    if abs(difference) < abs(min_diff):
                        min_diff = difference
        except KeyError:
            # API returns no data for some valid combinations. I'm skipping those.
            return 100000
        except ValueError:
            return 100000
        return min_diff

    # Function that finds delays for every bus stop that the given bus crossed between sample in
    # prev_bus and next_bus.
    def __bus_stops_in_one_sample(self, prev_bus: ZTMBus, next_bus: ZTMBus) -> dict:
        # If a bus travels with the speed of 90km/h for one minute, it will traverse 1500m.
        # So, below I'm splitting the distance that a bus completes by 9, and for each point on the
        # straight path between two points I'm looking for bus stops that it may have pass.
        # Additionally, I need to update time for that.
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
            if next_bus.line not in self.__bus_routes_data:
                # There was literally one time when API didn't send information about 4 buses,
                # so I keep track of that for statistics.
                self.__nr_of_unread_buses += 1
                break
            for route_code in self.__bus_routes_data[next_bus.line]:
                for bre in self.__bus_routes_data[next_bus.line][route_code]:
                    # Sometimes API doesn't send some data (in this case bus stop data),
                    # so here I'm handling bus stops that weren't sent by the API.
                    if (bre.team_nr not in self.__unread_stops or bre.bus_stop_nr
                            not in self.__unread_stops[bre.team_nr]):
                        try:
                            bs_data = self.__bus_stop_data[bre.team_nr][bre.bus_stop_nr]
                        except KeyError:
                            if bre.team_nr in self.__unread_stops:
                                self.__unread_stops[bre.team_nr].append(bre.bus_stop_nr)
                            else:
                                self.__unread_stops[bre.team_nr] = [bre.bus_stop_nr]
                            continue
                        # Locations are equal, if the distance between them is <= 175 meters.
                        if loc_c == bs_data.location:
                            delay = self.__calc_time_difference(next_bus.line, next_bus.brigade,
                                                                local_time_data, bs_data, route_code)
                            # Finding the smallest abs(delay), because a bus could stand on lights
                            # before arriving to the stop, and those lights could be closer to the bus stop
                            # than 175m, so we want to the delay that represents the bus being the closest
                            # to the bus stop.
                            if delay < 100000 and bs_data in found_bus_stops:
                                temp = found_bus_stops[bs_data]
                                if abs(delay) < abs(temp):
                                    found_bus_stops[bs_data] = delay
                                elif abs(delay) == abs(temp):
                                    found_bus_stops[bs_data] = max(delay, temp)
                            elif delay < 100000:
                                found_bus_stops[bs_data] = delay
            # Updating vectors and time.
            loc_c.longitude = loc_c.longitude + diff_x
            loc_c.latitude = loc_c.latitude + diff_y
            local_time_data += time_diff
        return found_bus_stops

    # Function that finds the sum of all delays for every bus stop as well as the number of busses
    # that arrived fo every bus stop.
    def calc_bus_stops_statistics(self) -> None:
        calculated_buses = {}
        for bus_nr in self.__bus_data:
            for vehicle_nr in self.__bus_data[bus_nr]:
                for i in range(len(self.__bus_data[bus_nr][vehicle_nr]) - 1):
                    curr_bus_data = self.__bus_data[bus_nr][vehicle_nr][i]
                    next_bus_data = self.__bus_data[bus_nr][vehicle_nr][i + 1]
                    found_bus_stops = self.__bus_stops_in_one_sample(curr_bus_data,
                                                                     next_bus_data)
                    if bus_nr not in calculated_buses:
                        calculated_buses[bus_nr] = {}
                    if vehicle_nr not in calculated_buses[bus_nr]:
                        calculated_buses[bus_nr][vehicle_nr] = {}
                    if next_bus_data.brigade not in calculated_buses[bus_nr][vehicle_nr]:
                        calculated_buses[bus_nr][vehicle_nr][next_bus_data.brigade] = {}
                    for key in found_bus_stops:
                        # I don't want to count three delays for one bus stop and one bus,
                        # so below is the logic for checking if the found bus stop weren't already
                        # paired with the given bus, and if so, we are looking for the smallest abs(delay)
                        # (which represents data being closest to the bus stop)/
                        if key in calculated_buses[bus_nr][vehicle_nr][next_bus_data.brigade]:
                            if (abs(calculated_buses[bus_nr][vehicle_nr][next_bus_data.brigade][key]) >
                                    found_bus_stops[key]):
                                # New abs(delay) is smaller so we need to update our mapping, as well as
                                # the sum of all delays.
                                self.__times_for_stops[key] -= (
                                    calculated_buses)[bus_nr][vehicle_nr][next_bus_data.brigade][key]
                                self.__times_for_stops[key] += found_bus_stops[key]
                                calculated_buses[bus_nr][vehicle_nr][next_bus_data.brigade][key] = found_bus_stops[key]
                        else:
                            calculated_buses[bus_nr][vehicle_nr][next_bus_data.brigade][key] = found_bus_stops[key]
                            if key in self.__times_for_stops:
                                self.__times_for_stops[key] += found_bus_stops[key]
                                self.__nr_of_buses_for_stops[key] += 1
                            else:
                                self.__times_for_stops[key] = found_bus_stops[key]
                                self.__nr_of_buses_for_stops[key] = 1

    # Function that calculates avg delays for every bus stop.
    def calc_average_delays(self) -> None:
        for key in self.__nr_of_buses_for_stops:
            new_key = key.team_name + '_' + key.post
            self.__avg_times_for_stops[new_key] = (float(self.__times_for_stops[key]) /
                                                   float(self.__nr_of_buses_for_stops[key]))

    # Function that dumps average delays data into the given file, but only as long as the
    # calculated data is between upper limits and lower limits (as long as they were
    # set by the user). This operation deletes data in __avg_times_for_stops and __times_for_stops.
    def dump_average_delays(self, file_to_dump: str, upper_limit: float = -1, lower_limit: float = 1) -> None:
        assert_file_extension(file_to_dump, '.csv')
        with open(file_to_dump, 'w', newline='', encoding='utf16') as file:
            data_headers = ['Bus_stop', 'Avg_time']
            csv_writer = csv.writer(file)
            csv_writer.writerow(data_headers)
            for data in sorted(self.__avg_times_for_stops, key=self.__avg_times_for_stops.get, reverse=True):
                if upper_limit != -1 and lower_limit != 1:
                    if upper_limit > self.__avg_times_for_stops[data] > lower_limit:
                        data_list = [data, str(self.__avg_times_for_stops[data])]
                        csv_writer.writerow(data_list)
                else:
                    data_list = [data, str(self.__avg_times_for_stops[data])]
                    csv_writer.writerow(data_list)
        self.__avg_times_for_stops.clear()
        self.__times_for_stops.clear()

    # Function that dumps the information about the number of buses that reached every bus stop
    # in the given .csv file stamp into the given file. This operation clears data in
    # __nr_of_buses_for_stops.
    def dump_nr_of_buses_for_each_stop(self, file_to_dump: str) -> None:
        assert_file_extension(file_to_dump, '.csv')
        with open(file_to_dump, 'w', newline='', encoding='utf16') as file:
            data_headers = ['Bus_stop', 'Nr_of_buses']
            csv_writer = csv.writer(file)
            csv_writer.writerow(data_headers)
            for bs in sorted (self.__nr_of_buses_for_stops, key=self.__nr_of_buses_for_stops.get, reverse=True):
                row = [bs.team_name + '_' + bs.post, self.__nr_of_buses_for_stops[bs]]
                csv_writer.writerow(row)
        self.__nr_of_buses_for_stops.clear()

    # Function that dumps the data associated with data errors from the API
    # into the given file. This operation clears all the data related to the
    # invalid stats.
    def dump_invalid_data_stats(self, file_to_dump: str) -> None:
        assert_file_extension(file_to_dump, '.csv')
        data_headers = ['Error_type', 'nr_of_entries']
        with open(file_to_dump, 'w', newline='', encoding='utf16') as file:
            csv_writer = csv.writer(file)
            csv_writer.writerow(data_headers)
            data_list = ['invalid_speeds', str(self.__nr_of_invalid_speeds)]
            csv_writer.writerow(data_list)
            data_list = ['invalid_times', str(self.__nr_of_invalid_times)]
            csv_writer.writerow(data_list)
            data_list = ['unread_busses', str(self.__nr_of_unread_buses)]
            csv_writer.writerow(data_list)
            nr_of_stops = 0
            for key in self.__unread_stops:
                nr_of_stops += len(self.__unread_stops[key])
            data_list = ['unreceived_bus_stops', nr_of_stops]
            csv_writer.writerow(data_list)
        self.__nr_of_invalid_speeds = 0
        self.__nr_of_invalid_times = 0
        self.__nr_of_unread_buses = 0
        self.__unread_stops.clear()
