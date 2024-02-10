import time
from math import cos, asin, sqrt, pi
import datetime as dt

import requests


class Location:
    __slots__ = ('longitude', 'latitude', 'street_name')

    def __init__(self, longitude, latitude, street_name=''):
        self.longitude = longitude
        self.latitude = latitude
        self.street_name = street_name
        # print(response.json()['results']['1']['street'])

    def distance(self, other):
        r = 6371  # km
        p = pi / 180
        a = (0.5 - cos((other.latitude - self.latitude) * p) / 2 + cos(self.latitude * p) * cos(other.latitude * p) *
             (1 - cos((other.longitude - self.longitude) * p)) / 2)
        return 2 * r * asin(sqrt(a))

    def __eq__(self, other):
        dist = self.distance(other)
        if dist <= 20000:
            return True
        else:
            return False

    def __ne__(self, other):
        return not (self == other)

    def find_street(self):
        if self.street_name == '':
            response = requests.post(
                'https://services.gugik.gov.pl/uug/?request=GetAddressReverse&location=POINT('
                + str(self.longitude) + ' ' + str(self.latitude) + ')&srid=4326')
            if response.json()['results'] is not None:
                self.street_name = response.json()['results']['1']['street']
            else:
                self.street_name = 'Unknown_location'

    def __hash__(self):
        return hash((self.latitude, self.latitude))

    def to_csv(self):
        result = [self.longitude, self.latitude, self.street_name]
        return result


class ZTM_bus:
    line: str
    location: Location
    vehicle_number: str
    brigade: str
    time_data: int
    street_name: str

    def __init__(self, line, longitude, latitude, vehicle_number, brigade, time_data, street_name=''):
        self.line = line
        self.location = Location(longitude, latitude, street_name)
        self.vehicle_number = vehicle_number
        self.brigade = brigade
        time_helper = time_data[11:]
        time_sec = int(time_helper[:2]) * 60
        time_sec += int(time_helper[3:5])
        time_sec *= 60
        time_sec += int(time_helper[6:])
        self.time_data = time_sec

    def to_csv(self):
        result = [self.line] + self.location.to_csv() + [self.vehicle_number, self.brigade, self.time_data]
        return result


class bus_stop:
    team_name: str
    street_id: str
    team: str
    post: str
    direction: str
    location: Location

    def __init__(self, team_name, street_id, team, post, direction, longitude, latitude):
        self.team_name = team_name
        self.street_id = street_id
        self.team = team
        self.post = post
        self.direction = direction
        self.location = Location(longitude, latitude)

    def __hash__(self):
        return hash((self.team_name, self.street_id, self.team,
                     self.post, self.direction, self.location))

    def to_csv(self):
        result = [self.team_name, self.street_id, self.team, self.post, self.direction] + self.location.to_csv()
        return result


class bus_for_stop:
    team: str
    post: str
    bus: str

    def __init__(self, team, post, bus):
        self.team = team
        self.post = post
        self.bus = bus

    def to_csv(self):
        result = [self.team, self.post, self.bus]
        return result


class bus_schedule_entry:
    brigade: str
    direction: str
    route: str
    time_data: int

    def __init__(self, brigade, direction, route, time_data):
        self.brigade = brigade
        self.direction = direction
        self.route = route
        self.time = time
        time_helper = time_data[11:]
        time_sec = int(time_helper[:2]) * 60
        time_sec += int(time_helper[3:5])
        time_sec *= 60
        time_sec += int(time_helper[6:])
        self.time_data = time_sec

    def to_csv(self):
        result = [self.brigade, self.direction, self.route, self.time_data]
        return result


class bus_route_entry:
    bus_nr: str
    route_code: str
    street_id: str
    team_nr: str
    type: str
    bus_stop_nr: str

    def __init__(self, bus_nr, route_code, street_id, team_nr, type, bus_stop_nr):
        self.bus_nr = bus_nr
        self.route_code = route_code
        self.street_id = street_id
        self.team_nr = team_nr
        self.type = type
        self.bus_stop_nr = bus_stop_nr

    def to_csv(self):
        result = [self.bus_nr, self.route_code, self.street_id, self.team_nr, self.type, self.bus_stop_nr]
        return result