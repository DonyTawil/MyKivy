__author__ = 'root'

from kivy.uix.widget import Widget
from kivy.properties import BooleanProperty
from random import randint


class SnakeFoo(Widget):
    is_eaten = BooleanProperty(False)

    def position(self, boundary_x, boundary_y):
        self.pos[0] = randint(0, boundary_x)
        self.pos[1] = randint(0, boundary_y)
