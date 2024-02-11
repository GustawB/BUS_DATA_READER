import pytest

from data_analyzer import data_analyzer
from data_holders import ZTM_bus


class TestDataAnalyzerClass:
    @pytest.fixture
    def expected_bus_locations(self):
        return {
            '666': {
                '2137': [ZTM_bus('666', '21.000293', '52.206126', '2137', '5', '2024-02-10 19:29:38'),
                         ZTM_bus('666', '21.001999', '52.219890', '2137', '5', '2024-02-10 19:30:41')],
                '5471': [ZTM_bus('666', '21.114995', '52.233576', '5471', '3', '2024-02-10 18:15:21'),
                         ZTM_bus('666', '21.114995', '52.233576', '5471', '3', '2024-02-10 18:17:21')]
            },

            '777': {
                '4220': [ZTM_bus('777', '21.1035602', '52.1273747', '4220', '7', '2024-02-10 19:39:38'),
                         ZTM_bus('777', '21.1039602', '52.1293747', '4220', '7', '2024-02-10 19:39:48')]
            },
            '888': {
                '6969': [ZTM_bus('888', '20.995331', '52.186255', '6969', '1', '2024-02-10 19:15:21'),
                         ZTM_bus('888', '20.995331', '52.1776255', '6969', '1', '2024-02-10 19:16:01')]
            }
        }

    @pytest.fixture
    def expected_schedules(self):
        return {
            '1000': {
                '01': {
                    '666': [
                        ['1', 'BLBL', 'TP-OST', '53460'],
                        ['2', 'BLBL', 'TP-OST', '54060'],
                        ['3', 'BLBL', 'TP-OST', '54660']
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

    def test_reading_bus_data(self, expected_bus_locations):
        da = data_analyzer()
        da.read_bus_data('test_files/test_bus_data.csv')
        data_dict = da.bus_data
        for bus in expected_bus_locations:
            assert bus in data_dict
            for vehicle in expected_bus_locations[bus]:
                assert vehicle in data_dict[bus]
                for i in range(len(expected_bus_locations[bus][vehicle])):
                    assert expected_bus_locations[bus][vehicle][i] == data_dict[bus][vehicle][i]

    def test_reading_schedules_data(self, expected_schedules):
        da = data_analyzer()
        da.read_schedules_data('test_files/schedules', 20)
        data_dict = da.schedules
        for team in expected_schedules:
            assert team in data_dict
            for post in expected_schedules[team]:
                assert post in data_dict[team]
                for bus in expected_schedules[team][post]:
                    assert bus in data_dict[team][post]
                    for i in range(len(expected_schedules[team][post][bus])):
                        assert expected_schedules[team][post][bus][i] == data_dict[team][post][bus][i]


    def test_nr_of_overspeeding_busses(self):
        da = data_analyzer()
        da.read_bus_data('test_files/test_bus_data.csv')
        assert da.calc_nr_of_overspeeding_busses() == 3
        assert da.nr_of_invalid_speeds == 1
        assert da.nr_of_invalid_times == 0
