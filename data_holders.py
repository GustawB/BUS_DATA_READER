import time
import geopy.distance


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

    def to_csv(self):
        result = [self.line, self.longitude, self.latitude, self.vehicle_number, self.brigade, self.time]
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


class Location:
    longitude: float
    latitude: float

    def __init__(self, longitude, latitude):
        self.longitude = longitude
        self.latitude = latitude

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

    def __hash__(self):
        return hash((self.latitude, self.latitude))
