class GeoPoint():
    def __init__(self, lat: float = 0.0, lon: float = 0.0, alt: float = 0.0):
        self.latitude = lat
        self.longitude = lon
        self.altitude = alt


class MissionObj():
    origin = GeoPoint()
    mission_waypoints = list() 

