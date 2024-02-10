import pytest
from unittest.mock import MagicMock, patch

from data_holders import ZTM_bus
from data_reader import data_reader


@pytest.fixture
def mock_bus_locations_req_1():
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
def mock_bus_locations_req_2():
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
        }
        ]
    }


@pytest.fixture
def expected_dict_1():
    return {
        '666': [ZTM_bus('666', '21.000293', '52.206126', '2137', '5', '2024-02-10 19:29:38'),
                ZTM_bus('666', '21.114995', '52.233576', '5471', '3', '2024-02-10 18:15:21')],
        '777': [ZTM_bus('777', '21.1035602', '52.1273747', '4220', '7', '2024-02-10 19:39:38')],
        '888': [ZTM_bus('888', '20.995331', '52.186255', '6969', '1', '2024-02-10 19:15:21')]
    }


@pytest.fixture
def expected_dict_2():
    return {
        '666': [ZTM_bus('666', '21.001999', '52.219890', '2137', '5', '2024-02-10 19:30:41'),
                ZTM_bus('666', '21.114995', '52.233576', '5471', '3', '2024-02-10 18:17:21')],
        '777': [ZTM_bus('777', '21.1039602', '52.1293747', '4220', '7', '2024-02-10 19:39:48')],
        '888': [ZTM_bus('888', '20.995331', '52.1776255', '6969', '1', '2024-02-10 19:16:01')]
    }


def test_bus_data_reading(mock_bus_locations_req_1, mock_bus_locations_req_2, expected_dict_1, expected_dict_2):
    with patch('data_reader.requests.get') as mock_get:
        mock_get.return_value = MagicMock(status_code=200)
        mock_get.return_value.json.return_value = mock_bus_locations_req_1

        dr = data_reader('random_apikey')
        dr.get_bus_data(1, 1)
        data_dict = dr.bus_data
        for key in expected_dict_1:
            assert key in data_dict
            for i in range(len(expected_dict_1[key])):
                assert expected_dict_1[key][i] == data_dict[key][i]

        mock_get.return_value.json.return_value = mock_bus_locations_req_2

        dr2 = data_reader('random_apikey')
        dr2.get_bus_data(1, 1)
        data_dict = dr2.bus_data
        for key in expected_dict_2:
            assert key in data_dict
            for i in range(len(expected_dict_2[key])):
                assert expected_dict_2[key][i] == data_dict[key][i]
