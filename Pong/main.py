from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import NumericProperty, ReferenceListProperty,\
     ObjectProperty, StringProperty
from kivy.vector import Vector
from kivy.clock import Clock
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from random import randint
from kivy.graphics import Color
from sys import exit


class PongPaddle(Widget):
    score = NumericProperty(0)

    def bounce_ball(self, ball):
        if self.collide_widget(ball):
            vx, vy = ball.velocity
            offset = (ball.center_y - self.center_y) / (self.height / 2)
            bounced = Vector(-1 * vx, vy)
            vel = bounced * 1.1
            ball.velocity = vel.x, vel.y + offset

class PongBall(Widget):
    velocity_x = NumericProperty(0)
    velocity_y = NumericProperty(0)

    velocity = ReferenceListProperty(velocity_x, velocity_y)

    def move(self):
        self.pos = Vector(*self.velocity) + self.pos

class PongGame(Widget):
    ball = ObjectProperty(None)
    player1 = ObjectProperty(None)
    player2 = ObjectProperty(None)
    who_wins = StringProperty("")
    is_menu = StringProperty("No menu")
    #def __init__(self, **kwargs):
    #    super(PongGame, self).__init__(**kwargs)
    #    self.menu = None


    def serve_ball(self, vel = (4, 0)):
        self.ball.center = self.center
        self.ball.velocity = vel

    def the_menu(self):
        self.ball.velocity = 0, 0
        self.menu = BoxLayout(orientation = "vertical", center_x = self.center_x, center_y = self.center_y)
        lbl = Label(text = "menu")
        self.menu.add_widget(lbl)
        btn1 = Button(text = "Restart", on_press = self.the_resume)
        btn1.bind(on_press = self.the_resume)
        btn2 = Button(text = "Exit", on_press = self.get_out)
        self.menu.add_widget(btn1)
        self.menu.add_widget(btn2)
        self.add_widget(self.menu)

    def the_resume(self, instance):  
        self.who_wins = ""
        self.player2.score = 0
        self.player1.score = 0
        self.menu.clear_widgets() #this is not working 
        self.remove_widget(self.menu) #Neither is this
        self.is_menu = "No menu"
        if self.who_wins == "Player 2 wins":
            vel = (-4, 0)
        else:
            vel = (4, 0)
        self.serve_ball(vel)

    def get_out(self, instance):
        exit()
            

    def update(self, dt):
        self.ball.move()

        self.player1.bounce_ball(self.ball)
        self.player2.bounce_ball(self.ball)

        if (self.ball.y < 0) or (self.ball.top > self.height):
            self.ball.velocity_y *= -1
        
        if self.ball.x < self.x:
            self.player2.score += 1
            self.serve_ball(vel = (4, 0))
        if self.ball.x > self.width:
            self.player1.score += 1
            self.serve_ball(vel = (-4, 0))

        if self.who_wins == "":
            if self.player2.score >= 1:
                self.who_wins = "Player 2 wins"
            elif self.player1.score >= 10:
                self.who_wins = "Player 1 wins"
        elif  self.is_menu == "No menu":
            self.is_menu = "menu"
            self.the_menu()

    def on_touch_move(self, touch):
        if touch.x < self.width / 3:
            self.player1.center_y = touch.y
        if touch.x > self.width - self.width / 3:
            self.player2.center_y = touch.y

class PongApp(App):
    def build(self):
        game = PongGame()
        game.serve_ball()
        Clock.schedule_interval(game.update, 1.0/60.0)
        return game

if __name__ == "__main__":
    PongApp().run()



