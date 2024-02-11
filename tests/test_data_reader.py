import os.path

import pytest
from unittest.mock import MagicMock, patch

from data_holders import ZTM_bus, bus_stop, bus_for_stop, bus_schedule_entry, bus_route_entry
from data_reader import data_reader


class TestDataReaderClass:
    @pytest.fixture
    def mock_bus_locations_1(self):
        return {
            "result": [{
                "Lines": "666",
                "Lon": "21.000293",
                "VehicleNumber": "2137",
                "Time": "2024-02-10 19:29:38",
                "Lat": "52.206126",
                "Brigade": "5"
            }, {
                "Lines": "777",
                "Lon": "21.1035602",
                "VehicleNumber": "4220",
                "Time": "2024-02-10 19:39:38",
                "Lat": "52.1273747",
                "Brigade": "7"
            }, {
                "Lines": "888",
                "Lon": "20.995331",
                "VehicleNumber": "6969",
                "Time": "2024-02-10 19:15:21",
                "Lat": "52.186255",
                "Brigade": "1"
            }, {
                "Lines": "666",
                "Lon": "21.114995",
                "VehicleNumber": "5471",
                "Time": "2024-02-10 18:15:21",
                "Lat": "52.233576",
                "Brigade": "3"
            }
            ]
        }

    @pytest.fixture
    def mock_bus_locations_2(self):
        return {
            "result": [{  # 1441 meters, 63 seconds
                "Lines": "666",
                "Lon": "21.001999",
                "VehicleNumber": "2137",
                "Time": "2024-02-10 19:30:41",
                "Lat": "52.219890",
                "Brigade": "5"
            }, {  # 212 meters, 10 seconds
                "Lines": "777",
                "Lon": "21.1039602",
                "VehicleNumber": "4220",
                "Time": "2024-02-10 19:39:48",
                "Lat": "52.1293747",
                "Brigade": "7"
            }, {  # 895 meters, 40 seconds
                "Lines": "888",
                "Lon": "20.995331",
                "VehicleNumber": "6969",
                "Time": "2024-02-10 19:16:01",
                "Lat": "52.1776255",
                "Brigade": "1"
            }, {  # 0 meters, 120 seconds
                "Lines": "666",
                "Lon": "21.114995",
                "VehicleNumber": "5471",
                "Time": "2024-02-10 18:17:21",
                "Lat": "52.233576",
                "Brigade": "3"
            }]
        }

    @pytest.fixture
    def mock_bus_stop_data(self):
        return {
            "result": [
                {
                    "values": [
                        {"value": "1000", "key": "zespol"},
                        {"value": "01", "key": "slupek"},
                        {"value": "BLBL", "key": "nazwa_zespolu"},
                        {"value": "2000", "key": "id_ulicy"},
                        {"value": "52.219890", "key": "szer_geo"},
                        {"value": "21.001999", "key": "dlug_geo"},
                        {"value": "ALA", "key": "kierunek"},
                        {"value": "2023-10-07 00:00:00.0", "key": "obowiazuje_od"}
                    ]
                },
                {
                    "values": [
                        {"value": "1001", "key": "zespol"},
                        {"value": "02", "key": "slupek"},
                        {"value": "LBLB", "key": "nazwa_zespolu"},
                        {"value": "2001", "key": "id_ulicy"},
                        {"value": "52.1293747", "key": "szer_geo"},
                        {"value": "21.1039602", "key": "dlug_geo"},
                        {"value": "BALA", "key": "kierunek"},
                        {"value": "2023-10-07 00:00:00.0", "key": "obowiazuje_od"}
                    ]
                },
                {
                    "values": [
                        {"value": "1002", "key": "zespol"},
                        {"value": "03", "key": "slupek"},
                        {"value": "BYYL", "key": "nazwa_zespolu"},
                        {"value": "2002", "key": "id_ulicy"},
                        {"value": "52.1776255", "key": "szer_geo"},
                        {"value": "20.995331", "key": "dlug_geo"},
                        {"value": "ABALA", "key": "kierunek"},
                        {"value": "2023-10-07 00:00:00.0", "key": "obowiazuje_od"}
                    ]
                }
            ]
        }

    @pytest.fixture
    def mock_bus_for_stops_data_1000_01(self):
        return {
            "result": [
                {
                    "values": [
                        {"value": "666", "key": "linia"}
                    ]
                },
                {
                    "values": [
                        {"value": "777", "key": "linia"}
                    ]
                }
            ]
        }

    @pytest.fixture
    def mock_bus_for_stops_data_1001_02(self):
        return {
            "result": [
                {
                    "values": [
                        {"value": "888", "key": "linia"}
                    ]
                },
            ]
        }

    @pytest.fixture
    def mock_bus_for_stops_data_1002_03(self):
        return {
            "result": [
                {
                    "values": [
                        {"value": "666", "key": "linia"}
                    ]
                },
            ]
        }

    @pytest.fixture
    def mock_schedules_1000_01_666(self):
        return {
            "result": [
                {
                    "values": [
                        {"value": "null", "key": "symbol_2"},
                        {"value": "null", "key": "symbol_1"},
                        {"value": "1", "key": "brygada"},
                        {"value": "BLBL", "key": "kierunek"},
                        {"value": "TP-OST", "key": "trasa"},
                        {"value": "14:51:00", "key": "czas"},
                    ]
                },
                {
                    "values": [
                        {"value": "null", "key": "symbol_2"},
                        {"value": "null", "key": "symbol_1"},
                        {"value": "2", "key": "brygada"},
                        {"value": "BLBL", "key": "kierunek"},
                        {"value": "TP-OST", "key": "trasa"},
                        {"value": "15:01:00", "key": "czas"},
                    ]
                },
                {
                    "values": [
                        {"value": "null", "key": "symbol_2"},
                        {"value": "null", "key": "symbol_1"},
                        {"value": "3", "key": "brygada"},
                        {"value": "BLBL", "key": "kierunek"},
                        {"value": "TP-OST", "key": "trasa"},
                        {"value": "15:11:00", "key": "czas"},
                    ]
                }
            ]
        }

    @pytest.fixture
    def mock_schedules_1000_01_777(self):
        return {
            "result": [
                {
                    "values": [
                        {"value": "null", "key": "symbol_2"},
                        {"value": "null", "key": "symbol_1"},
                        {"value": "4", "key": "brygada"},
                        {"value": "LBLB", "key": "kierunek"},
                        {"value": "TP-TSO", "key": "trasa"},
                        {"value": "04:16:00", "key": "czas"},
                    ]
                },
                {
                    "values": [
                        {"value": "null", "key": "symbol_2"},
                        {"value": "null", "key": "symbol_1"},
                        {"value": "5", "key": "brygada"},
                        {"value": "LBLB", "key": "kierunek"},
                        {"value": "TP-TSO", "key": "trasa"},
                        {"value": "05:16:00", "key": "czas"},
                    ]
                },
                {
                    "values": [
                        {"value": "null", "key": "symbol_2"},
                        {"value": "null", "key": "symbol_1"},
                        {"value": "6", "key": "brygada"},
                        {"value": "LBLB", "key": "kierunek"},
                        {"value": "TP-TSO", "key": "trasa"},
                        {"value": "06:16:00", "key": "czas"},
                    ]
                }
            ]
        }

    @pytest.fixture
    def mock_schedules_1001_02_888(self):
        return {
            "result": [
                {
                    "values": [
                        {"value": "null", "key": "symbol_2"},
                        {"value": "null", "key": "symbol_1"},
                        {"value": "7", "key": "brygada"},
                        {"value": "BBBB", "key": "kierunek"},
                        {"value": "TP-STO", "key": "trasa"},
                        {"value": "18:39:00", "key": "czas"},
                    ]
                },
                {
                    "values": [
                        {"value": "null", "key": "symbol_2"},
                        {"value": "null", "key": "symbol_1"},
                        {"value": "8", "key": "brygada"},
                        {"value": "BBBB", "key": "kierunek"},
                        {"value": "TP-STO", "key": "trasa"},
                        {"value": "18:45:00", "key": "czas"},
                    ]
                },
                {
                    "values": [
                        {"value": "null", "key": "symbol_2"},
                        {"value": "null", "key": "symbol_1"},
                        {"value": "9", "key": "brygada"},
                        {"value": "BBBB", "key": "kierunek"},
                        {"value": "TP-STO", "key": "trasa"},
                        {"value": "18:51:00", "key": "czas"},
                    ]
                }
            ]
        }

    @pytest.fixture
    def mock_schedules_1002_03_666(self):
        return {
            "result": [
                {
                    "values": [
                        {"value": "null", "key": "symbol_2"},
                        {"value": "null", "key": "symbol_1"},
                        {"value": "1", "key": "brygada"},
                        {"value": "BLBL", "key": "kierunek"},
                        {"value": "TP-OST", "key": "trasa"},
                        {"value": "16:51:00", "key": "czas"},
                    ]
                },
                {
                    "values": [
                        {"value": "null", "key": "symbol_2"},
                        {"value": "null", "key": "symbol_1"},
                        {"value": "2", "key": "brygada"},
                        {"value": "BLBL", "key": "kierunek"},
                        {"value": "TP-OST", "key": "trasa"},
                        {"value": "17:01:00", "key": "czas"},
                    ]
                },
                {
                    "values": [
                        {"value": "null", "key": "symbol_2"},
                        {"value": "null", "key": "symbol_1"},
                        {"value": "3", "key": "brygada"},
                        {"value": "BLBL", "key": "kierunek"},
                        {"value": "TP-OST", "key": "trasa"},
                        {"value": "17:11:00", "key": "czas"},
                    ]
                }
            ]
        }

    @pytest.fixture
    def mock_bus_routes(self):
        return {
            "result": {
                "666": {
                    "TP-OST": {
                        "1": {
                            "odleglosc": 100,
                            "ulica_id": "2000",
                            "nr_zespolu": "1000",
                            "typ": "2",
                            "nr_przystanku": "01"
                        },
                        "2": {
                            "odleglosc": 3000,
                            "ulica_id": "2002",
                            "nr_zespolu": "1002",
                            "typ": "1",
                            "nr_przystanku": "03"
                        }
                    }
                },
                "777": {
                    "TP-TSO": {
                        "1": {
                            "odleglosc": 0,
                            "ulica_id": "2000",
                            "nr_zespolu": "1000",
                            "typ": "7",
                            "nr_przystanku": "01"
                        }
                    }
                },
                "888": {
                    "TP-STO": {
                        "1": {
                            "odleglosc": 0,
                            "ulica_id": "2001",
                            "nr_zespolu": "1001",
                            "typ": "9",
                            "nr_przystanku": "02"
                        }
                    }
                }
            }
        }

    @pytest.fixture
    def expected_bus_locations(self):
        return {
            '666': [ZTM_bus('666', '21.000293', '52.206126', '2137', '5', '2024-02-10 19:29:38'),
                    ZTM_bus('666', '21.114995', '52.233576', '5471', '3', '2024-02-10 18:15:21'),
                    ZTM_bus('666', '21.001999', '52.219890', '2137', '5', '2024-02-10 19:30:41'),
                    ZTM_bus('666', '21.114995', '52.233576', '5471', '3', '2024-02-10 18:17:21')],
            '777': [ZTM_bus('777', '21.1035602', '52.1273747', '4220', '7', '2024-02-10 19:39:38'),
                    ZTM_bus('777', '21.1039602', '52.1293747', '4220', '7', '2024-02-10 19:39:48')],
            '888': [ZTM_bus('888', '20.995331', '52.186255', '6969', '1', '2024-02-10 19:15:21'),
                    ZTM_bus('888', '20.995331', '52.1776255', '6969', '1', '2024-02-10 19:16:01')]
        }

    @pytest.fixture
    def expected_dict_2(self):
        return {
            '666': [ZTM_bus('666', '21.001999', '52.219890', '2137', '5', '2024-02-10 19:30:41'),
                    ZTM_bus('666', '21.114995', '52.233576', '5471', '3', '2024-02-10 18:17:21')],
            '777': [ZTM_bus('777', '21.1039602', '52.1293747', '4220', '7', '2024-02-10 19:39:48')],
            '888': [ZTM_bus('888', '20.995331', '52.1776255', '6969', '1', '2024-02-10 19:16:01')]
        }

    @pytest.fixture
    def expected_bus_stop(self):
        return {
            "BLBL": [bus_stop('BLBL', '2000', '1000', '01', 'ALA', 21.001999, 52.219890)],
            "LBLB": [bus_stop('LBLB', '2001', '1001', '02', 'BALA', 21.1039602, 52.1293747)],
            "BYYL": [bus_stop('BYYL', '2002', '1002', '03', 'ABALA', 20.995331, 52.1776255)]
        }

    @pytest.fixture
    def expected_bus_for_stop(self):
        return {
            '1000': [bus_for_stop('1000', '01', '666'),
                     bus_for_stop('1000', '01', '777')],
            '1001': [bus_for_stop('1001', '02', '888')],
            '1002': [bus_for_stop('1002', '03', '666')]
        }

    @pytest.fixture
    def expected_schedules(self):
        return {
            "1000": {
                "01": {
                    "666": [bus_schedule_entry('1', 'BLBL', 'TP-OST', '14:51:00'),
                            bus_schedule_entry('2', 'BLBL', 'TP-OST', '15:01:00'),
                            bus_schedule_entry('3', 'BLBL', 'TP-OST', '15:11:00')],
                    "777": [bus_schedule_entry('4', 'LBLB', 'TP-TSO', '04:16:00'),
                            bus_schedule_entry('5', 'LBLB', 'TP-TSO', '05:16:00'),
                            bus_schedule_entry('6', 'LBLB', 'TP-TSO', '06:16:00'), ]
                }
            },
            "1001": {
                "02": {
                    "888": [bus_schedule_entry('7', 'BBBB', 'TP-STO', '18:39:00'),
                            bus_schedule_entry('8', 'BBBB', 'TP-STO', '18:45:00'),
                            bus_schedule_entry('9', 'BBBB', 'TP-STO', '18:51:00')]
                }
            },
            "1002": {
                "03": {
                    "666": [bus_schedule_entry('1', 'BLBL', 'TP-OST', '16:51:00'),
                            bus_schedule_entry('2', 'BLBL', 'TP-OST', '17:01:00'),
                            bus_schedule_entry('3', 'BLBL', 'TP-OST', '17:11:00')]
                }
            }
        }

    @pytest.fixture
    def expected_bus_routes(self):
        return {
            "666": {
                "TP-OST": {
                    1: bus_route_entry("666", "TP-OST",
                                       "2000", "1000", "2", "01"),
                    2: bus_route_entry("666", "TP-OST",
                                       "2002", "1002", "1", "03")
                }
            },
            "777": {
                "TP-TSO": {
                    1: bus_route_entry("777", "TP-TSO",
                                       "2000", "1000", "7", "01")
                }
            },
            "888": {
                "TP-STO": {
                    1: bus_route_entry("888", "TP-STO",
                                       "2001", "1001", "9", "02")
                }
            }
        }

    def test_bus_data_reading(self, mock_bus_locations_1,
                              mock_bus_locations_2,
                              expected_bus_locations):
        with patch('data_reader.requests.get') as mock_get:
            mock_get.return_value = MagicMock(status_code=200)
            mock_get.return_value.json.return_value = mock_bus_locations_1
            dr = data_reader('random_apikey')
            dr.get_bus_data(1, 1)
            mock_get.return_value.json.return_value = mock_bus_locations_2
            dr.get_bus_data(1, 1)
            data_dict = dr.bus_data
            assert len(expected_bus_locations) == len(data_dict)
            for bus in expected_bus_locations:
                assert bus in data_dict
                assert len(expected_bus_locations[bus]) == len(data_dict[bus])
                for i in range(len(expected_bus_locations[bus])):
                    assert expected_bus_locations[bus][i] == data_dict[bus][i]
            if not os.path.isdir('test_files'):
                os.mkdir('test_files')
            dr.dump_bus_data('test_files/test_bus_data.csv')

    def test_bus_stop_data_reading(self, mock_bus_stop_data, expected_bus_stop):
        with patch('data_reader.requests.get') as mock_get:
            mock_get.return_value = MagicMock(status_code=200)
            mock_get.return_value.json.return_value = mock_bus_stop_data
            dr = data_reader('random_apikey')
            dr.get_stops_data()
            data_dict = dr.bus_stop_data
            for key in expected_bus_stop:
                assert key in data_dict
                for i in range(len(expected_bus_stop[key])):
                    assert expected_bus_stop[key][i] == data_dict[key][i]
            if not os.path.isdir('test_files'):
                os.mkdir('test_files')
            dr.dump_stops_data('test_files/test_bus_stops.csv')

    def test_bus_for_stops_data_reading(self, mock_bus_for_stops_data_1000_01,
                                        mock_bus_for_stops_data_1001_02,
                                        mock_bus_for_stops_data_1002_03,
                                        expected_bus_for_stop):
        with patch('data_reader.requests.get') as mock_get:
            mock_get.return_value = MagicMock(status_code=200)
            mock_get.return_value.json.side_effect = [mock_bus_for_stops_data_1000_01,
                                                      mock_bus_for_stops_data_1001_02,
                                                      mock_bus_for_stops_data_1002_03]
            dr = data_reader('random_apikey')
            dr.get_busses_for_stops('test_files/test_bus_stops.csv')
            data_dict = dr.busses_for_stops
            assert len(data_dict) == 3
            for key in expected_bus_for_stop:
                assert key in data_dict
                for i in range(len(expected_bus_for_stop[key])):
                    assert expected_bus_for_stop[key][i] == data_dict[key][i]
            dr.dump_busses_for_stops('test_files/test_busses_for_stops.csv')

    def test_schedules_data_reading(self, mock_schedules_1000_01_666,
                                    mock_schedules_1000_01_777,
                                    mock_schedules_1001_02_888,
                                    mock_schedules_1002_03_666,
                                    expected_schedules):
        with patch('data_reader.requests.get') as mock_get:
            mock_get.return_value = MagicMock(status_code=200)
            mock_get.return_value.json.side_effect = [mock_schedules_1000_01_666,
                                                      mock_schedules_1000_01_777,
                                                      mock_schedules_1001_02_888,
                                                      mock_schedules_1002_03_666]
            dr = data_reader('random_apikey')
            dr.get_bus_schedules('test_files/test_busses_for_stops.csv')
            data_dict = dr.schedules
            for team in expected_schedules:
                assert team in data_dict
                for post in expected_schedules[team]:
                    assert post in data_dict[team]
                    for bus in expected_schedules[team][post]:
                        assert bus in data_dict[team][post]
                        for i in range(len(expected_schedules[team][post][bus])):
                            assert expected_schedules[team][post][bus][i] == data_dict[team][post][bus][i]
            dr.dump_schedules('test_files')

    def test_bus_routes_data_reading(self,mock_bus_routes,
                                     expected_bus_routes):
        with patch('data_reader.requests.get') as mock_get:
            mock_get.return_value = MagicMock(status_code=200)
            mock_get.return_value.json.return_value = mock_bus_routes
            dr = data_reader('random_apikey')
            dr.get_bus_routes()
            data_dict = dr.bus_routes
            for bus in expected_bus_routes:
                assert bus in data_dict
                for route in expected_bus_routes[bus]:
                    assert route in data_dict[bus]
                    for index in expected_bus_routes[bus][route]:
                        assert index in data_dict[bus][route]
                        assert expected_bus_routes[bus][route][index] == data_dict[bus][route][index]
            if not os.path.isdir('test_files'):
                os.mkdir('test_files')
            dr.dump_bus_routes('test_files/test_bus_routes.csv')

    def test_time_parser(self):
        dr = data_reader('random_apikey')
        assert dr.time_parser('24:00:00') == '00:00:00'
        assert dr.time_parser('25:00:00') == '01:00:00'
        assert dr.time_parser('26:00:00') == '02:00:00'
        assert dr.time_parser('27:00:00') == '03:00:00'
        assert dr.time_parser('28:00:00') == '04:00:00'
        assert dr.time_parser('29:00:00') == '05:00:00'
        assert dr.time_parser('15:23:32') == '15:23:32'
