import geopy

from data_analyzer import data_analyzer
from data_reader import data_reader

if __name__ == '__main__':
    dt = data_reader('afd497b5-83e7-4ecf-8c98-cd1805aa16c9')
    #dt.get_bus_data(2, 1)
    #dt.dump_bus_data('bus_data.csv')

    da = data_analyzer()
    da.read_bus_data('bus_data.csv')
    #print(da.bus_data['225']['1008'][0].latitude)
    #print(da.bus_data['225']['1008'][0].longitude)
    #print(da.bus_data['225']['1008'][1].latitude)
    #print(da.bus_data['225']['1008'][1].longitude)
    coords1 = (da.bus_data['225']['1008'][0].latitude, da.bus_data['225']['1008'][0].longitude)
    coords2 = (da.bus_data['225']['1008'][1].latitude, da.bus_data['225']['1008'][1].longitude)
    dist = geopy.distance.geodesic(coords1, coords2).m
    #print(dist)
    #print(' ')
    #print(da.calc_nr_of_overspeeding_busses(1))

    #dt.get_stops_data()
    #dt.dump_stops_data('bus_stop_data.csv')

    dt.get_busses_for_stops('bus_stop_data.csv')

    dt.get_bus_schedules('bus_for_stops.csv')
    dt.dump_schedules()


