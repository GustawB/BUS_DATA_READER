import geopy
import requests
import os

from data_analyzer import data_analyzer
from data_reader import data_reader

if __name__ == '__main__':
    dt = data_reader('afd497b5-83e7-4ecf-8c98-cd1805aa16c9')
    #dt.get_streets()
    #dt.dump_streets('streets.csv')
    #dt.get_bus_data(2, 1)
    #dt.dump_bus_data('bus_data.csv')
    dt.get_bus_routes()
    dt.dump_bus_routes('bus_routes_data.csv')

    da = data_analyzer()
    #da.read_bus_data('bus_data.csv')
    #print(da.calc_nr_of_overspeeding_busses(1))
    #da.calc_data_for_overspeed_percentages(1)
    #da.calc_overspeed_percentages()
    #print(da.overspeed_percentages)
    #da.calc_times_for_stops()

    #dt.get_stops_data()
    #dt.dump_stops_data('bus_stop_data.csv')

    #dt.get_busses_for_stops('bus_stop_data.csv')
    #dt.dump_busses_for_stops('bus_for_stops.csv')

    #dt.get_bus_schedules('bus_for_stops.csv')
    #dt.dump_schedules()
    #da.calc_data_for_overspeed_percentages(1)
    #da.calc_overspeed_percentages()
    #print(da.overspeed_percentages)





