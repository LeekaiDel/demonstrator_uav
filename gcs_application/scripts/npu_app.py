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
import threading


class Container(BoxLayout):
    butt_set_waypoint = ObjectProperty()
    butt_set_home = ObjectProperty()
    butt_clear = ObjectProperty()
    map_layer = ObjectProperty()
    butt_bar = ObjectProperty()
    paint_layer = ObjectProperty()
    
    rad = 10

    set_waypoint = False
    waypoint_array_gps = list()

    # def my_callback(self, dt):
    #     print("rrr")

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
        self.paint_layer.canvas.clear()
        points = list()
        if(self.waypoint_array_gps):
            for marker in self.waypoint_array_gps:
                points.append((marker.x + 5, marker.y + 5))
            with self.paint_layer.canvas:
                Color(1, 0, 0, 1)
                # for point in points:
                    # Ellipse(pos = (point[0] - self.rad / 2, point[1] - self.rad / 2), size = (self.rad, self.rad))
                Line(points = points, width = 2)

    def set_waypoint_cb(self):
        self.set_waypoint = not self.set_waypoint
        print("Press Set_WayPoint")
    
    def set_home_cb(self):
        print("Press Set_Home")

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