import time


class ZTM_bus:
    line: str
    longitude: float
    latitude: float
    vehicle_number: str
    brigade: str
    time: time.struct_time

    def __init__(self, line, longitude, latitude, vehicle_number, brigade, time):
        self.line = line
        self.longitude = longitude
        self.latitude = latitude
        self.vehicle_number = vehicle_number
        self.brigade = brigade
        self.time = time