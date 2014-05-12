__author__ = 'root'
from kivy.uix.widget import Widget
from kivy.graphics import Line, Color
from kivy.properties import ListProperty


class SnakePalette(Widget):

    def clear(self, snake_head_pos, touch_list):
        self.canvas.clear()
        snake_head_pos.extend(touch_list)
        self.point_list = snake_head_pos
        with self.canvas:
            Line(points = self.point_list)

