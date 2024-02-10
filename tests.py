import pytest
from unittest.mock import MagicMock, patch


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
            "Lines": "999",
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
        "result": [{    # 1441 meters, 63 seconds
            "Lines": "666",
            "Lon": "21.001999",
            "VehicleNumber": "2137",
            "Time": "2024-02-10 19:30:41",
            "Lat": "52.219890",
            "Brigade": "5"
        }, {    # 212 meters, 10 seconds
            "Lines": "777",
            "Lon": "21.1039602",
            "VehicleNumber": "4220",
            "Time": "2024-02-10 19:39:48",
            "Lat": "52.1293747",
            "Brigade": "7"
        }, {    # 895 meters, 40 seconds
            "Lines": "888",
            "Lon": "20.995331",
            "VehicleNumber": "6969",
            "Time": "2024-02-10 19:16:01",
            "Lat": "52.1776255",
            "Brigade": "1"
        }, {    # 0 meters, 120 seconds
            "Lines": "999",
            "Lon": "21.114995",
            "VehicleNumber": "5471",
            "Time": "2024-02-10 18:17:21",
            "Lat": "52.233576",
            "Brigade": "3"
        }
        ]
    }
