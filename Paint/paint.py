from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.properties import ListProperty, ObjectProperty
from kivy.uix.gridlayout import GridLayout
from kivy.graphics import Color, Ellipse, Line
from random import random


class color_choice(Widget):
    color = ListProperty([])

    def __init__(self, la_couleur, **kwargs):
        super(color_choice, self).__init__(**kwargs)
        self.color = la_couleur


class MyPaintWidget(Widget):
    the_grid = ObjectProperty(None)
    la_couleur2 = ListProperty([])

    def __init__(self, **kwargs):
        super(MyPaintWidget, self).__init__(**kwargs)
        self.the_grid = GridLayout(cols = 2, row_force_default = True, row_default_height = 30)
        self.get_colours((1, 0, 0), (0, 1, 0), (0, 0, 1), (0, 1, 1), (1, 1, 1))
        #self.add_widget(self.the_grid) #this caused a very weird error but fixed it by adding the widget in the app

    def get_colours(self, *args):
        self.the_grid.pos = [200, 200]
        self.the_grid.size = [200, 200]
        for arg in args:
            a_color = color_choice(arg)
            self.the_grid.add_widget(a_color)

    def on_touch_down(self, touch):
        la_limit = 0.25 # To not make it too dark
        for arg in self.the_grid.children:
            print self.the_grid.pos
            print arg
            print arg.size
            print arg.color
            print arg.pos
            if arg.collide_point(*touch.pos):
                self.change_color(arg)
                break
        if self.la_couleur2 == []:
            la_couleur = random(), random(), random()

            while (la_couleur[0] <  la_limit or la_couleur[1] < la_limit or la_couleur[2] < la_limit):
                la_couleur = random(), random(), random()

        with self.canvas:

            if self.la_couleur2 == []:
                Color(*(la_couleur))
            else:
                Color(*(self.la_couleur2))
            d = 30.0
            Ellipse(pos = (touch.x - d / 2, touch.y - d / 2), size = (d, d))
            touch.ud['line'] = Line(points = (touch.x, touch.y))

    def change_color(self, the_color_widget):
        if the_color_widget.color != (1, 1, 1):
            self.la_couleur2 = the_color_widget.color
        else:
            self.la_couleur2 = []


    def on_touch_move(self, touch):
        touch.ud['line'].points += [touch.x, touch.y]



class MyPaintApp(App):
    def build(self):
        #self.get_colours((1, 0, 0), (0, 1, 0), (0, 0, 1), (0, 1, 1), (1, 1, 1))
        parent = Widget()
        #parent.add_widget(self.the_grid)
        the_painter = MyPaintWidget()
        clear_button = Button(text = "Clear")
        clear_button.size = [50, 50]

        def clear_stuff(obj):
            the_painter.canvas.clear()
        clear_button.bind(on_release = clear_stuff)
        #the_painter.add_widget(clear_button)  When I did this you can see the button but you can't press
        parent.add_widget(clear_button)
        parent.add_widget(the_painter)
        return parent

if __name__ == "__main__":
    MyPaintApp().run()
