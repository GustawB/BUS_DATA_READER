import geopy.distance
from math import cos, asin, sqrt, pi
import requests
import os

from data_analyzer import DataAnalyzer
from data_reader import DataReader
from data_visualizer import data_visualizer

if __name__ == '__main__':
    dt = DataReader('afd497b5-83e7-4ecf-8c98-cd1805aa16c9')
    # dt.get_streets()
    # dt.dump_streets('streets.csv')
    dt.get_bus_data(2, 60)
    print('sex')
    dt.dump_bus_data('bus_data.csv', 600)
    # dt.get_bus_routes()
    # dt.dump_bus_routes('bus_routes_data.csv')

    coords1 = (20.995331, 52.186255)
    coords2 = (20.995331, 52.1776255)
    dist = geopy.distance.geodesic(coords1, coords2).m
    #print(dist/40*3600/1000)
    print(dist)
    r = 6371  # km
    p = pi / 180
    a = (0.5 - cos((coords2[0] - coords1[0]) * p) / 2 + cos(coords1[0] * p) * cos(coords2[0] * p) *
         (1 - cos((coords2[1] - coords1[1]) * p)) / 2)
    dist = 2 * r * asin(sqrt(a))
    print(dist*1000)

    da = DataAnalyzer()
    da.read_schedules_data('schedules', 9)
    #print(da.schedules)
    print('a')
    da.read_bus_data('bus_data.csv')
    print('b')
    da.read_bus_stop_data('bus_stop_data.csv')
    print('c')
    da.read_bus_routes_data('bus_routes_data.csv')
    print('d')
    #print(da.calc_nr_of_overspeeding_busses())
    #print(da.nr_of_invalid_times)
    #print(da.nr_of_invalid_speeds)
    #da.calc_data_for_overspeed_percentages()
    #da.calc_overspeed_percentages('overspeed_data.csv')
    #print(da.overspeed_percentages)
    da.calc_times_for_stops()
    da.calc_average_delays('avg_delays.csv', 600.0, -300.0)
    #print(da.nr_of_unread_buses)
    #print(da.avg_times_for_stops)

    # dt.get_stops_data()
    # dt.dump_stops_data('bus_stop_data.csv')

    # dt.get_busses_for_stops('bus_stop_data.csv')
    # dt.dump_busses_for_stops('bus_for_stops.csv')

    # dt.get_bus_schedules('bus_for_stops.csv')
    # dt.dump_schedules()
    # da.calc_data_for_overspeed_percentages(1)
    # da.calc_overspeed_percentages()
    # print(da.overspeed_percentages)

    #dv = data_visualizer('overspeed_data.csv', 'Overspeed percentages for streets', 0, 1)
    #dv.print_data()
