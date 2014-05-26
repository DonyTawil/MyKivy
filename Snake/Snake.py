__author__ = 'root'

from kivy.uix.widget import Widget
from kivy.properties import NumericProperty, ListProperty, ReferenceListProperty, ObjectProperty, BooleanProperty
from kivy.core.window import Window
from kivy.vector import Vector
from kivy.graphics import Line
from dirline import SnakePalette
from snakepart import SnakePart
from math import pi, cos, sin
from lines import BoundaryLine
from scipy.interpolate import interp1d
import numpy as np

##Maybe use sets to remove duplicates A set has only unique elements list(set(foo))

#some global constants
snake_part_size = 10, 10
snake_globe_size = 50, 50
#Velocity_Norm for the snake head  #To remove this
Velocity_Norm = 2.5
#Update time
the_delta_time = float(1) / 60
background_color = [0, 1, 0]
#length when snake divides himself
divide_length = 12
#initial length
initial_length = 6


class Snake(Widget):
    """Widget made of a composition of multiple SnakePart"""
    color = ListProperty([1, 1, 1])
    direction_line = ListProperty([])
    next_position = ListProperty([])
    snake_palette = ObjectProperty(None)
    snake_head = ObjectProperty(None)
    new_head = BooleanProperty(False)
    do_draw = BooleanProperty(True)
    #Property to check if snake has currently
    #a part outside
    is_outside = BooleanProperty(False)
    #bl = BoundaryLine instance
    bl = ObjectProperty(None)
    #Points to interpolate
    touch_pointsi = ListProperty([])

    def __init__(self, **kwargs):
        super(Snake, self).__init__(**kwargs)
        self.snake_parts = []     # have to decide whether or not to use the children's list instead
        # Snake globe is an invisible circle, used to create a greater area for the player to
        # touch, so that he can guide the snake
        self.snake_globe = ObjectProperty(None)
        self.snake_palette = SnakePalette()
        self.bl = BoundaryLine()
        self.add_widget(self.bl)

    def initial_parts(self, n):
        for i in range(n):

            the_snake_part = SnakePart(self.color, snake_part_size)
            self.add_widget(the_snake_part)
            self.snake_parts.append(the_snake_part)
            self.snake_head = self.snake_parts[0]

            if i == 0:
                self.snake_globe = SnakePart(background_color, snake_globe_size)
                self.add_widget(self.snake_palette)
                self.add_widget(self.snake_globe)

    def check_tail(self):  # Not sure if still need this function
        #Checks if snake tail has crossed boundary to change
        #position of the snake
        snake_tail = self.snake_parts[-1]
        if snake_tail.check_out_of_window():
            return True

    def check_snake_inside(self):
        #Checks if any part of the snake has crossed boundary
        #If all the parts are inside it returns true
        for part in self.snake_parts:
            if part.check_out_of_window():
                return False
        else:
            return True

    def check_head(self):
        #Checks if snake head has crossed boundary
        snake_head = self.snake_parts[0]
        boundary = snake_head.check_out_of_window()
        if boundary:
            return True

    def initial_pos(self):
        snake_head = self.snake_parts[0]
        snake_head.pos = Window.center
        snake_head.velocity = [1, 0]
        for index in range(1, len(self.snake_parts)):
            snake_part = self.snake_parts[index]
            snake_part.pos[1] = snake_head.pos[1]
            snake_part.pos[0] = snake_head.pos[0] - index * snake_part.size[0]

    def assign_head_dir_velocity(self):
        if self.next_position:
            self.snake_head.velocity = (self.next_position[0] - self.snake_head.center_x)\
                , (self.next_position[1] - self.snake_head.center_y)
        else:
            #if no next position just keep the same velocity
            pass

    def assign_head_velocity(self):
        snake_head = self.snake_parts[0]
        # If there is still a direction to be followed
        if self.direction_line:
            #if self.next_position is empty or snake has just collided with next position
            if not self.next_position or snake_head.collide_point(self.next_position[0], self.next_position[1]):
                self.next_position = [self.direction_line.pop(0), self.direction_line.pop(0)]
                self.assign_head_dir_velocity()

        if not self.direction_line and self.next_position:
            #So that if snake passes next_point while touch_is_down
            #Pc stops drawing
            if snake_head.collide_point(self.next_position[0], self.next_position[1]):
                self.do_draw = False

        #So that the new head will move in the
        #right direction
        ##Fix this function
        if self.new_head:
            self.new_head = False
            self.assign_head_dir_velocity()

        self.snake_parts[0].normalize_velocity()

    def assign_velocity(self, index):
        #Have to fix this damn function, Fixed:removed norm / delta_time
        if index == 0:
            self.assign_head_velocity()
            return

        #For each snake_part assign its a velocity so that it follows the following snake_part
        snake_part = self.snake_parts[index]
        prev = Vector(*self.snake_parts[index - 1].pos)
        current = Vector(*snake_part.pos)

        #The norm has to be equal to the difference in:
        # the snakes pos and the diameter of each snake_part i.e the distance
        #That should be between each snake part
        norm = prev - current
        snake_part.velocity = norm
        norm = norm.length() - snake_part_size[0]

        #In case a part become too close to another one, don't let it move backwards
        #Though this might never be happening
        if norm < 0:
            norm = 0
        snake_part.normalize_velocity(norm)

    def update(self, dt):
        for i in range(len(self.snake_parts)):
            snake_part = self.snake_parts[i]
            self.assign_velocity(i)
            snake_part.move(dt)

        if self.is_outside:
            self.other_side()

        if self.check_head():
            self.is_outside = True

        self.snake_globe.center = self.snake_parts[0].center
        self.snake_globe.pos[0] %= Window.width
        self.snake_globe.pos[1] %= Window.height

        if self.direction_line or self.next_position:
            #Code to update the direction line
            snake_head_pos = self.snake_parts[0].center[:]
            self.snake_palette.clear(snake_head_pos, self.direction_line)

        self.bl.set_lcoord(self.snake_head.center, self.snake_head.velocity)

        self.did_snake_suicide()

    def other_side(self):
        if self.check_snake_inside():
            for i in self.snake_parts:
                i.change_pos()
            self.is_outside = False

    def on_touch_down(self, touch):
        if self.snake_globe.collide_point(*touch.pos):
            touch.grab(self)
            #allow to draw direction lines again
            self.do_draw = True
            with self.snake_palette.canvas:
                touch.ud['line'] = Line(points = (touch.x, touch.y))
            self.next_position = []
            self.direction_line = touch.ud['line'].points

    def did_snake_suicide(self):
        #update this function to check for collision with other
        #snakes
        for i in range(1, len(self.snake_parts)):
            if self.did_snake_part_collide(i):
                print "Die"

    def did_snake_part_collide(self, index):
        snake_part_center = self.snake_parts[index].center
        if self.snake_head.collide_point(*snake_part_center):
            return True

    def remove_cons(self, list1, list2):
        #function that removes consecutives duplicates iff
        #there are duplicates in both list1 and list2 at the
        #same position
        x = [list1[0]]
        y = [list2[0]]
        print list1, list2
        print "len",len(list1)
        print "len2", len(list2)
        if len(list1) > 1:
            for i in range(1, len(list1)):
                if (list1[i], list2[i]) != (list1[i - 1], list2[i - 1]):
                    x.append(list1[i])
                    y.append(list2[i])
        return x, y

    def on_touch_move(self, touch):
        ##Now have to fix this function
        if touch.grab_current is self and self.do_draw:
            touch.ud['line'].points += [touch.x, touch.y]
            self.direction_line.extend([touch.x, touch.y])
            x, y = self.extract(touch.ud['line'].points)
            x, y = self.remove_cons(x, y)
            if len(x) > 4:
                interp = np.polyfit(x, y, 2)
                interp = np.poly1d(interp)

                xstart = int(x[0])
                xend = int(x[-1])
                list = []
                for i in range(xstart, xend):
                    list += [i, int(interp(i))]
                touch.ud['line'].points = list
                self.direction_line = list

    def extract(self, list):
        x = [i for i in list if list.index(i) % 2 == 0]
        y = [i for i in list if i not in x]
        return x, y

    def check_if_ate(self, parent):
        if parent.da_food.is_eaten:
            return
        if self.snake_head.collide_widget(parent.da_food):
            parent.da_food.is_eaten = True
            new_snake_head = SnakePart(self.color, snake_part_size)
            new_snake_head.pos = parent.da_food.pos
            new_snake_head.velocity = self.snake_head.velocity
            self.add_widget(new_snake_head)
            self.snake_parts.insert(0, new_snake_head)
            self.snake_head = self.snake_parts[0]
            self.new_head = True

    def should_divide_snake(self):
        if len(self.snake_parts) == divide_length:
            return True

    def remove_parts(self):
        for i in range(0, initial_length):
            snake_part = self.snake_parts[-1]
            self.remove_widget(snake_part)
            self.snake_parts.pop(-1)