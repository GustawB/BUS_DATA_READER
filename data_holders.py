import time
import geopy.distance

import requests


class Location:
    __slots__ = ('longitude', 'latitude', 'street_name')

    def __init__(self, longitude, latitude, street_name=''):
        self.longitude = longitude
        self.latitude = latitude
        self.street_name = street_name
        #print(response.json()['results']['1']['street'])

    def __eq__(self, other):
        coords1 = (self.latitude, self.longitude)
        coords2 = (other.latitude, other.longitude)
        dist = geopy.distance.geodesic(coords1, coords2).m
        if dist <= 200:
            return True
        else:
            return False

    def __ne__(self, other):
        return not (self == other)

    def distance(self, other):
        coords1 = (self.latitude, self.longitude)
        coords2 = (other.latitude, other.longitude)
        return geopy.distance.geodesic(coords1, coords2).m

    def find_street(self):
        if self.street_name == '':
            response = requests.post(
                'https://services.gugik.gov.pl/uug/?request=GetAddressReverse&location=POINT('
                + str(self.longitude) + ' ' + str(self.latitude) + ')&srid=4326')
            if response.json()['results'] is not None:
                self.street_name = response.json()['results']['1']['street']
            else:
                self.street_name = 'None'


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
    time_data: time.struct_time
    street_name: str

    def __init__(self, line, longitude, latitude, vehicle_number, brigade, time_data, street_name=''):
        self.line = line
        self.location = Location(longitude, latitude, street_name)
        self.vehicle_number = vehicle_number
        self.brigade = brigade
        self.time_data = time_data

    def to_csv(self):
        result = [self.line] + self.location.to_csv() + [self.vehicle_number, self.brigade, self.time_data]
        return result


class bus_stop:
    team_name: str
    street_id: str
    team: str
    post: str
    direction: str
    longitude: float
    latitude: float

    def __init__(self, team_name, street_id, team, post, direction, longitude, latitude):
        self.team_name = team_name
        self.street_id = street_id
        self.team = team
        self.post = post
        self.direction = direction
        self.longitude = longitude
        self.latitude = latitude

    def to_csv(self):
        result = [self.team_name, self.street_id, self.team, self.post, self.direction, self.longitude, self.latitude]
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
    time: time.struct_time

    def __init__(self, brigade, direction, route, time):
        self.brigade = brigade
        self.direction = direction
        self.route = route
        self.time = time

    def to_csv(self):
        result = [self.brigade, self.direction, self.route, self.time]
        return result


class street_holder:
    street_name: str
    location: Location

    def __init__(self, street_name, longitude, latitude):
        self.street_name = street_name
        self.location = Location(longitude, latitude)

    def to_csv(self):
        result = [self.street_name] + self.location.to_csv()
        return result
