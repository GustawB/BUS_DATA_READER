import pytest

from warsawbuspy.analyzers.data_analyzer import DataAnalyzer
from warsawbuspy.holders.data_holders import ZTMBus, BusStop, BusRouteEntry


class TestDataAnalyzerClass:
    @pytest.fixture
    def expected_bus_locations(self):
        return {
            '666': {
                '2137': [ZTMBus('666', '21.000293', '52.206126', '2137', '5', '2024-02-10 19:29:38'),
                         ZTMBus('666', '21.001999', '52.219890', '2137', '5', '2024-02-10 19:30:41')],
                '5471': [ZTMBus('666', '21.114995', '52.233576', '5471', '3', '2024-02-10 18:15:21'),
                         ZTMBus('666', '21.114995', '52.233576', '5471', '3', '2024-02-10 18:17:21')]
            },

            '777': {
                '4220': [ZTMBus('777', '21.1035602', '52.1273747', '4220', '7', '2024-02-10 19:39:38'),
                         ZTMBus('777', '21.1039602', '52.1293747', '4220', '7', '2024-02-10 19:39:48')]
            },
            '888': {
                '6969': [ZTMBus('888', '20.995331', '52.186255', '6969', '1', '2024-02-10 19:15:21'),
                         ZTMBus('888', '20.995331', '52.1776255', '6969', '1', '2024-02-10 19:16:01')]
            }
        }

    @pytest.fixture
    def expected_schedules(self):
        return {
            '1000': {
                '01': {
                    '666': [
                        ['5', 'BLBL', 'TP-OST', '53460'],
                        ['5', 'BLBL', 'TP-OST', '54060'],
                        ['5', 'BLBL', 'TP-OST', '54660']
                    ],
                    '777': [
                        ['4', 'LBLB', 'TP-TSO', '15360'],
                        ['5', 'LBLB', 'TP-TSO', '18960'],
                        ['6', 'LBLB', 'TP-TSO', '22560']
                    ]
                }
            },
            '1001': {
                '02': {
                    '888': [
                        ['7', 'BBBB', 'TP-STO', '67140'],
                        ['8', 'BBBB', 'TP-STO', '67500'],
                        ['9', 'BBBB', 'TP-STO', '67860']
                    ]
                }
            },
            '1002': {
                '03': {
                    '666': [
                        ['1', 'BLBL', 'TP-OST', '60660'],
                        ['2', 'BLBL', 'TP-OST', '61260'],
                        ['3', 'BLBL', 'TP-OST', '61860']
                    ]
                }
            }
        }

    @pytest.fixture
    def expected_bus_stops(self):
        return {
            '1000': {
                '01': BusStop('BLBL', '2000', '1000', '01', 'ALA', 21.001999, 52.21989)
            },
            '1001': {
                '02': BusStop('LBLB', '2001', '1001', '02', 'BALA', 21.1039602, 52.1293747)
            },
            '1002': {
                '03': BusStop('BYYL', '2002', '1002', '03', 'ABALA', 20.995331, 52.1776255)
            }
        }

    @pytest.fixture
    def expected_bus_routes(self):
        return {
            '666': {
                'TP-OST': [
                    BusRouteEntry('666', 'TP-OST', '2000', '1000', '2', '01'),
                    BusRouteEntry('666', 'TP-OST', '2002', '1002', '1', '03')
                ]
            },
            '777': {
                'TP-TSO': [
                    BusRouteEntry('777', 'TP-TSO', '2000', '1000', '7', '01')
                ]
            },
            '888': {
                'TP-STO': [
                    BusRouteEntry('888', 'TP-STO', '2001', '1001', '9', '02')
                ]
            }
        }

    @pytest.fixture
    def expected_avg_delays(self):
        return {'BLBL_01': 15518.0}

    def test_reading_bus_data(self, expected_bus_locations):
        da = DataAnalyzer()
        da.read_bus_data('test_files/test_bus_data.csv')
        data_dict = da.bus_data
        for bus in expected_bus_locations:
            assert bus in data_dict
            for vehicle in expected_bus_locations[bus]:
                assert vehicle in data_dict[bus]
                for i in range(len(expected_bus_locations[bus][vehicle])):
                    assert expected_bus_locations[bus][vehicle][i] == data_dict[bus][vehicle][i]

    def test_reading_schedules_data(self, expected_schedules):
        da = DataAnalyzer()
        da.read_schedules_data('test_files/schedules')
        data_dict = da.schedules
        for team in expected_schedules:
            assert team in data_dict
            for post in expected_schedules[team]:
                assert post in data_dict[team]
                for bus in expected_schedules[team][post]:
                    assert bus in data_dict[team][post]
                    for i in range(len(expected_schedules[team][post][bus])):
                        assert expected_schedules[team][post][bus][i] == data_dict[team][post][bus][i]

    def test_reading_bus_stop_data(self, expected_bus_stops):
        da = DataAnalyzer()
        da.read_bus_stop_data('test_files/test_bus_stops.csv')
        data_dict = da.bus_stop_data
        for team in expected_bus_stops:
            assert team in data_dict
            for post in expected_bus_stops[team]:
                assert post in data_dict[team]
                assert expected_bus_stops[team][post] == data_dict[team][post]

    def test_reading_bus_routes_data(self, expected_bus_routes):
        da = DataAnalyzer()
        da.read_bus_routes_data('test_files/test_bus_routes.csv')
        data_dict = da.bus_routes_data
        for bus in expected_bus_routes:
            assert bus in data_dict
            for route in expected_bus_routes[bus]:
                assert route in data_dict[bus]
                for i in range(len(expected_bus_routes[bus][route])):
                    assert expected_bus_routes[bus][route][i] == data_dict[bus][route][i]

    def test_nr_of_overspeeding_busses(self):
        da = DataAnalyzer()
        da.read_bus_data('test_files/test_bus_data.csv')
        assert da.calc_nr_of_overspeeding_busses() == 3
        assert da.nr_of_invalid_speeds == 0
        assert da.nr_of_invalid_times == 0
        da.calc_overspeed_percentages()
        da.dump_overspeed_percentages('test_files/test_overspeed_percentages.csv',
                                      'test_files/test_overspeed_locations.geojson')

    def test_avg_delays(self, expected_avg_delays):
        da = DataAnalyzer()
        da.read_bus_data('test_files/test_bus_data.csv')
        da.read_bus_stop_data('test_files/test_bus_stops.csv')
        da.read_bus_routes_data('test_files/test_bus_routes.csv')
        da.read_schedules_data('test_files/schedules')
        da.calc_bus_stops_statistics()
        da.calc_average_delays('test_files/test_results.csv')
        assert da.avg_times_for_stops == expected_avg_delays
        da.dump_average_delays('test_files/test_avg_delays.csv')

