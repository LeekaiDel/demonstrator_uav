import json


class GeoPoint():
    def __init__(self, lat: float = 0.0, lon: float = 0.0, alt: float = 0.0):
        self.latitude = lat
        self.longitude = lon
        self.altitude = alt


class Mission():
    def __init__(self):
        self.origin = GeoPoint()
        self.mission_waypoints = list()
        self.time_stamp = None

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4)


class Telemetry():
    def __init__(self, lat: float = 0.0, lon: float = 0.0, alt: float = 0.0, azimute: float = 0.0, home_point: float = 0.0):
        self.latitude = lat
        self.longitude = lon
        self.altitude = alt
        self.azimute = azimute
        self.home_point = home_point
