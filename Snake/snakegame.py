__author__ = 'root'
##Program To do list

#Add collision: Not done, only made collision with snake with itself, done

#Have a problem with Die Gonna work on it bit by bit

#Try to make did_snake_part_collide and collide_function in snakegame one
#have to draw the transparent territory

#Have to make more clear when there is a collision

#When snake is outside and I guide it, it chooses the long road rather
#than the short one

#Have a problem with assign_head_dir: Think I fixed it make sure later

#When snakes eats a food by itself it changes direction

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import NumericProperty, ListProperty, ReferenceListProperty, ObjectProperty, BooleanProperty
from kivy.core.window import Window
from kivy.vector import Vector
from kivy.clock import Clock
from kivy.graphics import Line
from dirline import SnakePalette
from snakefoo import SnakeFoo
from snakepart import SnakePart
from Snake import Snake


#some global constants
snake_part_size = 10, 10
snake_globe_size = 50, 50
#Velocity_Norm for the snake head  #To remove this
Velocity_Norm = 2.5
#Update time
the_delta_time = float(1) / 60
background_color = [0, 1, 0]
#initial length
initial_length = 6


class SnakeSandbox(Widget):
    da_snakes = ListProperty([])
    #Class to hold all the snakes

    def create_snakes(self):
        the_Snake = Snake()
        the_Snake.initial_parts(initial_length)
        the_Snake.initial_pos()
        self.add_widget(the_Snake)
        self.da_snakes.append(the_Snake)
        #Put the following part in a function
        self.da_food = SnakeFoo()
        self.da_food.size = snake_part_size
        self.da_food.position(Window.width, Window.height)
        self.add_widget(self.da_food)

    def update(self, dt):
        for snake in self.children:
            if isinstance(snake, Snake):
                snake.check_if_ate(self)
                snake.update(dt)
                if snake.should_divide_snake():
                    self.divide_snake(snake)
            elif isinstance(snake, SnakeFoo):
                if snake.is_eaten:
                    snake.position(Window.width, Window.height)
                    snake.is_eaten = False

        #Checking collision of snakes
        da_snakes_len = len(self.da_snakes)
        for i in range(da_snakes_len):
            snake = self.da_snakes[i]
            #Check if snake collided with itself
            snake.did_snake_suicide()
            #Check if snake collided with other snake
            for j in range(i+1, da_snakes_len):
                self.did_snake_collide(snake, self.da_snakes[j])

    def did_snake_collide(self, snake, snake_i):
        snake_head = snake.snake_head
        for snake_part in snake_i.snake_parts:
            snake_part_center = snake_part.center
            if snake_head.collide_point(*snake_part_center):
                print "Die by collision"
                return None  # Just in case have to replace this by True

    def divide_snake(self, snake):
        new_snake = Snake()
        new_snake.initial_parts(initial_length)
        self.derived_from(new_snake, snake)
        self.add_widget(new_snake)
        self.da_snakes.append(new_snake)

    def derived_from(self, new_snake, old_snake):
        old_head = old_snake.snake_parts[0]
        new_snake.snake_parts[0].velocity = Vector(-old_head.velocity_x, -old_head.velocity_y)
        for i in range(1, initial_length + 1):
            new_snake.snake_parts[i - 1].pos = old_snake.snake_parts[-i].pos
            #new_snake.snake_parts[i - 1].velocity = -Vector(*old_snake.snake_parts[-1].velocity)
        old_snake.remove_parts()


class SnakeApp(App):
    def build(self):
        widget = SnakeSandbox()
        widget.create_snakes()
        Clock.schedule_interval(widget.update, the_delta_time)
        return widget

if __name__ == "__main__":
    SnakeApp().run()
