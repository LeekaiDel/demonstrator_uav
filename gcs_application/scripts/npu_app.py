from turtle import width
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy_garden.mapview import MapView, MapMarkerPopup
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.graphics import Color, Ellipse, Line
from kivy.core.window import Window
from kivy.properties import ObjectProperty
from kivy.graphics.instructions import InstructionGroup
# from kivy.graphics.vertex_instructions import Line
from kivy.clock import Clock
import msgs
import threading
import zmq
import pickle
import msgs
import time
import zmq_wrapper_lib
import json

class Container(BoxLayout):
    def __init__(self, **kwargs):
        super(Container, self).__init__(**kwargs) 
        """       
        self.butt_set_waypoint
        self.butt_send
        self.butt_clear
        self.map_layer
        self.butt_bar
        self.paint_layer
        """
        self.host_telemetry = "localhost"
        self.port_telemetry = "5555"

        self.host_mission_manager = "192.168.88.229" 
        self.port_mission_manager = "8100"

        self.drone_nav = msgs.Telemetry()
        self.drone_marker = MapMarkerPopup(source = 'drone_icon.png')
        
        self.pub_mission = zmq_wrapper_lib.Client(ip = self.host_mission_manager, 
                                                    port = self.port_mission_manager)
        
        self.rad = 10

        self.set_waypoint = False
        self.waypoint_array_gps = list()
        
        self.mission = msgs.Mission()

        telem_thrd = threading.Thread(target = self.telemetry_thread, daemon = True)
        telem_thrd.start()
    
    def telemetry_thread(self):
        context = zmq.Context()
        socket = context.socket(zmq.REQ)
        socket.connect("tcp://" + self.host_telemetry + ":" + self.port_telemetry)
        print("Connect to server telemetry")
        
        while True:
            socket.send(b"")
            telemetry_massage = socket.recv()
            telemetry_translate = pickle.loads(telemetry_massage)
            self.drone_nav.latitude = telemetry_translate.latitude
            self.drone_nav.longitude = telemetry_translate.longitude
            self.drone_nav.azimute = telemetry_translate.azimute
            self.lable.text = "lat: " + str(telemetry_translate.latitude) + "\n" + "lon: " + str(telemetry_translate.longitude)
            # print(self.drone_nav)
 

    def on_touch_up(self, touch):
        if(self.set_waypoint) and (touch.button == 'left'):
            if(touch.y > self.butt_bar.size[1]):
                map_marker = MapMarkerPopup(
                    source = 'waypoint_10x10.png',
                    lat = self.map_layer.get_latlon_at(touch.x, touch.y - self.butt_bar.size[1] - 5)[0],
                    lon = self.map_layer.get_latlon_at(touch.x, touch.y - self.butt_bar.size[1])[1]) 
                self.waypoint_array_gps.append(map_marker)
                print("click ", len(self.waypoint_array_gps))
                self.map_layer.add_marker(map_marker)
                # self.draw_lines(None)


    def draw_markers(self, dt):
        # if self.drone_marker is not None:
        #     self.map_layer.remove_marker(self.drone_marker)
        self.paint_layer.canvas.clear()
        if self.drone_marker.lat == 0.0:
            self.drone_marker.lat = self.drone_nav.latitude
            self.drone_marker.lon = self.drone_nav.longitude

            self.map_layer.add_marker(self.drone_marker)
        
        else:
            self.drone_marker.lat = self.drone_nav.latitude
            self.drone_marker.lon = self.drone_nav.longitude
        self.map_layer.do_update(None)

        points = list()
        if(self.waypoint_array_gps):
            for marker in self.waypoint_array_gps:
                points.append((marker.x + 5, marker.y + 5))
            with self.paint_layer.canvas:
                Color(0, 0, 1, 0.5)
                # for point in points:
                # Ellipse(pos = (point[0] - self.rad / 2, point[1] - self.rad / 2), size = (self.rad, self.rad))
                Line(points = points, width = 2)


    def set_waypoint_cb(self):
        self.set_waypoint = not self.set_waypoint
        print("Press Set_WayPoint")
    

    def send_cb(self):
        print("Press Send Mission")
        if self.waypoint_array_gps:
            self.mission.time = time.time()
            for point in self.waypoint_array_gps:
                self.mission.mission_waypoints.append(msgs.GeoPoint(lat = point.lat, lon = point.lon)) #

            for point in self.mission.mission_waypoints:
                print(point)

            self.pub_mission.data_to_send = self.mission.toJSON()
            self.pub_mission.startClient()
            self.mission = msgs.Mission()


    def clear_cb(self):
        self.paint_layer.canvas.clear()
        for marker in self.waypoint_array_gps:
            self.map_layer.remove_marker(marker)
        self.waypoint_array_gps.clear()
        print("Press Set_Clear")


class NpuApp(App):
    def build(self): 
        container = Container()
        Clock.schedule_interval(container.draw_markers, 0.001)
        return container


if __name__ == "__main__":
    NpuApp().run()