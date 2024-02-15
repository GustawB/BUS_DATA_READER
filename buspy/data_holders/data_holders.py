from math import cos, asin, sqrt, pi

import requests


# Class responsible for holding the location, and finding the street tied to this location by
# fetching the data from the services.gugik.gov.pl API.
class Location:
    __slots__ = ('__longitude', '__latitude', '__street_name')

    def __init__(self, longitude, latitude, street_name=''):
        self.__longitude = longitude
        self.__latitude = latitude
        self.__street_name = street_name
        # print(response.json()['results']['1']['street'])

    def __eq__(self, other):
        dist = self.distance(other)
        return dist <= 175.0

    def __ne__(self, other):
        return not (self == other)

    def __hash__(self):
        return hash((self.latitude, self.latitude))

    @property
    def longitude(self):
        return self.__longitude

    @longitude.setter
    def longitude(self, new_value):
        self.__longitude = new_value

    @property
    def latitude(self):
        return self.__latitude

    @latitude.setter
    def latitude(self, new_value):
        self.__latitude = new_value

    @property
    def street_name(self):
        return self.__street_name

    # Function that calculates the distance between this location and the given one.
    def distance(self, other):
        r = 6371  # km
        p = pi / 180
        a = (0.5 - cos((other.longitude - self.__longitude) * p) / 2 + cos(self.__longitude * p) * cos(
            other.longitude * p) *
             (1 - cos((other.latitude - self.__latitude) * p)) / 2)
        return 2 * r * asin(sqrt(a)) * 1000

    # By default, the street name is empty. But, if user calls for it, find_street() will
    # fetch the location's data from the services.gugik.gov.pl API to extract the street name.
    def find_street(self):
        if self.street_name == '':
            response = requests.post(
                'https://services.gugik.gov.pl/uug/?request=GetAddressReverse&location=POINT('
                + str(self.longitude) + ' ' + str(self.latitude) + ')&srid=4326')
            if response.json()['results'] is not None:
                if response.json()['results']['1']['street'] is not None:
                    self.__street_name = response.json()['results']['1']['street']
                else:
                    self.__street_name = 'Unknown_location'
            else:
                self.__street_name = 'Unknown_location'

    # Converts class fields into the list.
    def to_csv(self):
        result = [self.longitude, self.latitude, self.street_name]
        return result


class ZTMBus:
    __slots__ = ('__line', '__location', '__vehicle_number', '__brigade', '__time_data', '__street_name')

    def __init__(self, line, longitude, latitude, vehicle_number, brigade, time_data, should_convert_time=True,
                 street_name=''):
        self.__line = line
        self.__location = Location(float(longitude), float(latitude), street_name)
        self.__vehicle_number = vehicle_number
        self.__brigade = brigade
        if should_convert_time:
            time_helper = time_data[11:]
            time_sec = int(time_helper[:2]) * 60
            time_sec += int(time_helper[3:5])
            time_sec *= 60
            time_sec += int(time_helper[6:])
            self.__time_data = time_sec
        else:
            self.__time_data = int(time_data)

    def __eq__(self, other):
        return (self.line == other.line and
                self.location == other.location and
                self.vehicle_number == other.vehicle_number and
                self.brigade == other.brigade and
                self.time_data == other.time_data)

    @property
    def line(self):
        return self.__line

    @property
    def location(self):
        return self.__location

    @property
    def vehicle_number(self):
        return self.__vehicle_number

    @property
    def brigade(self):
        return self.__brigade

    @property
    def time_data(self):
        return self.__time_data

    # Converts class fields into the list.
    def to_csv(self):
        result = [self.line] + self.location.to_csv() + [self.vehicle_number, self.brigade, self.time_data]
        return result


class BusStop:
    __slots__ = ('__team_name', '__street_id', '__team', '__post', '__direction', '__location')

    def __init__(self, team_name, street_id, team, post, direction, longitude, latitude):
        self.__team_name = team_name
        self.__street_id = street_id
        self.__team = team
        self.__post = post
        self.__direction = direction
        self.__location = Location(longitude, latitude)

    def __eq__(self, other):
        return (self.team_name == other.team_name and
                self.street_id == other.street_id and
                self.team == other.team and
                self.post == other.post and
                self.direction == other.direction and
                self.location == other.location)

    def __hash__(self):
        return hash((self.team_name, self.street_id, self.team,
                     self.post, self.direction, self.location))

    @property
    def team_name(self):
        return self.__team_name

    @property
    def street_id(self):
        return self.__street_id

    @property
    def team(self):
        return self.__team

    @property
    def post(self):
        return self.__post

    @property
    def direction(self):
        return self.__direction

    @property
    def location(self):
        return self.__location

    # Converts class fields into the list.
    def to_csv(self):
        result = [self.team_name, self.street_id, self.team, self.post, self.direction] + self.location.to_csv()
        return result


class BusForStop:
    __slots__ = ('__team', '__post', '__bus')

    def __init__(self, team, post, bus):
        self.__team = team
        self.__post = post
        self.__bus = bus

    def __eq__(self, other):
        return (self.team == other.team and
                self.post == other.post and
                self.bus == other.bus)

    @property
    def team(self):
        return self.__team

    @property
    def post(self):
        return self.__post

    @property
    def bus(self):
        return self.__bus

    # Converts class fields into the list.
    def to_csv(self):
        result = [self.team, self.post, self.bus]
        return result


class BusScheduleEntry:
    __slots__ = ('__brigade', '__direction', '__route', '__time_data')

    def __init__(self, brigade, direction, route, time_data):
        self.__brigade = brigade
        self.__direction = direction
        self.__route = route
        time_sec = int(time_data[:2]) * 60
        time_sec += int(time_data[3:5])
        time_sec *= 60
        time_sec += int(time_data[6:])
        self.__time_data = time_sec

    def __eq__(self, other):
        return (self.brigade == other.brigade and
                self.direction == other.direction and
                self.route == other.route and
                self.time_data == other.time_data)

    @property
    def brigade(self):
        return self.__brigade

    @property
    def direction(self):
        return self.__direction

    @ property
    def route(self):
        return self.__route

    @property
    def time_data(self):
        return self.__time_data

    # Converts class fields into the list.
    def to_csv(self):
        result = [self.brigade, self.direction, self.route, self.time_data]
        return result


class BusRouteEntry:
    __slots__ = ('__bus_nr', '__route_code', '__street_id', '__team_nr', '__type', '__bus_stop_nr')

    def __init__(self, bus_nr, route_code, street_id, team_nr, stop_type, bus_stop_nr):
        self.__bus_nr = bus_nr
        self.__route_code = route_code
        self.__street_id = street_id
        self.__team_nr = team_nr
        self.__type = stop_type
        self.__bus_stop_nr = bus_stop_nr

    def __eq__(self, other):
        return (self.bus_nr == other.bus_nr and
                self.route_code == other.route_code and
                self.street_id == other.street_id and
                self.team_nr == other.team_nr and
                self.type == other.type and
                self.bus_stop_nr == other.bus_stop_nr)

    @property
    def bus_nr(self):
        return self.__bus_nr

    @property
    def route_code(self):
        return self.__route_code

    @property
    def street_id(self):
        return self.__street_id

    @property
    def team_nr(self):
        return self.__team_nr

    @property
    def type(self):
        return self.__type

    @property
    def bus_stop_nr(self):
        return self.__bus_stop_nr

    # Converts class fields into the list.
    def to_csv(self):
        result = [self.bus_nr, self.route_code, self.street_id, self.team_nr, self.type, self.bus_stop_nr]
        return result
