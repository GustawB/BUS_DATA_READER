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

    def __str__(self):
        result = str([self.line, self.longitude, self.latitude, self.vehicle_number, self.brigade, self.time])
        return result

    def to_csv(self):
        result = [self.line, self.longitude, self.latitude, self.vehicle_number, self.brigade, self.time]
        return result


class Location:
    longitude: float
    latitude: float
    Longitude_: float