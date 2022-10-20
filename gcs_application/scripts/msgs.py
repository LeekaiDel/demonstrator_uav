class GeoPoint:
    def __init__(self, lat: float = 0.0, lon: float = 0.0, alt: float = 0.0):
        self.latitude = lat
        self.longitude = lon
        self.altitude = alt


class Mission:
    time = float()
    origin = GeoPoint()
    mission_waypoints = dict()  # GeoPoint()


class Telemetry:
    def __init__(self, lat: float = 0.0, lon: float = 0.0, alt: float = 0.0, azimute: float = 0.0, home_point: float = 0.0):
        self.latitude = lat
        self.longitude = lon
        self.altitude = alt
        self.azimute = azimute
        self.home_point = home_point

