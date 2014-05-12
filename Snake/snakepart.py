__author__ = 'root'
from kivy.uix.widget import Widget
from kivy.core.window import Window
from kivy.properties import NumericProperty, ReferenceListProperty, ListProperty
from kivy.vector import Vector
from math import fabs

#Velocity_Norm for the snake head
Velocity_Norm = 2.5
#some global constants
snake_part_size = 10, 10


class SnakePart(Widget):
    #size = ListProperty(snake_part_size)
    velocity_x = NumericProperty(0)
    velocity_y = NumericProperty(0)
    velocity = ReferenceListProperty(velocity_x, velocity_y)
    #Color of the snakePart
    color = ListProperty([0, 0, 0])

    def __init__(self, color, snake_part_size, **kwargs):
        self.size = snake_part_size
        super(SnakePart, self).__init__(**kwargs)
        self.color = color

    def move(self, time):
        #It only works if independent of time else it cause some problems
        #because dt isn't fixed so can't get norm right
        self.pos = Vector(*self.pos) + Vector(*self.velocity)

    def normalize_velocity(self, norm = Velocity_Norm):
        #let the module of the velocity be equal to norm
        self.velocity = Vector(*self.velocity).normalize() * norm

    def change_pos(self):
        self.pos[0] = self.pos[0] % Window.width
        self.pos[1] = self.pos[1] % Window.height

    def check_out_of_window(self): # Not sure if need this. No I do need it
        #Checks if part is out of window
        #This function is wrong I need to fix this
        position = self.pos
        radius = snake_part_size[0]
        #We check position[i] % width, only when a part
        # smaller than 2 * radius is the part stilled considered outside
        width = Window.width
        height = Window.height

        boolean_val = fabs(position[0]) % width < 2 * radius
        boolean_val2 = fabs(position[1]) % height < 2 * radius

        if boolean_val or boolean_val2:
            return True
