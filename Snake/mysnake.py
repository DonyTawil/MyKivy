__author__ = 'root'

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import NumericProperty, ListProperty, ReferenceListProperty
from kivy.core.window import Window
from kivy.vector import Vector
from kivy.clock import Clock

#some global constants
snake_part_size = 10, 10
Velocity_Norm = 10


class SnakePart(Widget):
    part_size = ListProperty(snake_part_size)
    velocity_x = NumericProperty(0)
    velocity_y = NumericProperty(0)
    velocity = ReferenceListProperty(velocity_x, velocity_y)
    #Color of the snakePart
    color = ListProperty([0, 0, 0])

    def __init__(self, color, **kwargs):
        super(SnakePart, self).__init__(**kwargs)
        self.color = color

    def move(self, time):
        self.pos = Vector(*self.pos) + Vector(*self.velocity) * time

    def normalize_velocity(self):
        self.velocity = Vector(*self.velocity).normalize() * Velocity_Norm


class Snake(Widget):
    """Widget made of a composition of multiple SnakePart"""
    color = ListProperty([1, 1, 1])

    def __init__(self, **kwargs):
        super(Snake, self).__init__(**kwargs)
        self.snake_parts = []     # have to decide whether or not to use the children's list instead

    def initial_parts(self, n):
        for i in range(n):
            the_snake_part = SnakePart(self.color)
            self.add_widget(the_snake_part)
            self.snake_parts.append(the_snake_part)

    def initial_pos(self):
        snake_head = self.snake_parts[0]
        snake_head.pos = Window.center
        snake_head.velocity = [0, 1]
        for index in range(1, len(self.snake_parts)):
            snake_part = self.snake_parts[index]
            print snake_part.color
            snake_part.pos[1] = snake_head.pos[1]
            snake_part.pos[0] = snake_head.pos[0] - index * snake_part.part_size[0]

    def assign_velocity(self):
        #have to fix this function
        self.snake_parts[0].normalize_velocity()
        #For each snake_part assign its a velocity so that it follows the following snake_part
        for i in range(1, len(self.snake_parts)):
            snake_part = self.snake_parts[i]
            prev_snake_part_pos = self.snake_parts[i - 1].pos
            snake_part.velocity = Vector(*prev_snake_part_pos) - Vector(*snake_part.pos)
            snake_part.normalize_velocity()

    def update(self, dt):
        self.assign_velocity()
        for snake in self.snake_parts:
            snake.move(dt)



class SnakeApp(App):
    def build(self):
        widget = Snake()
        widget.initial_parts(10)
        widget.initial_pos()
        Clock.schedule_interval(widget.update, 1 / 60)
        return widget

if __name__ == "__main__":
    SnakeApp().run()
