__author__ = 'root'

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.properties import ListProperty, ObjectProperty, NumericProperty
from kivy.uix.gridlayout import GridLayout
from kivy.core.window import Window
from kivy.graphics import Color, Ellipse, Line, Rectangle
from random import random


class ColorChoice(Widget):
    color = ListProperty([0, 0, 0])

    def __init__(self, la_couleur, **kwargs):
        super(ColorChoice, self).__init__(**kwargs)
        self.color = la_couleur

#The class where everything is drawn to
class MyPaintPalette(Widget):
    pass



class MyPaintWidget(Widget):
    palette = ObjectProperty(None)
    the_grid = ObjectProperty(None)
    la_couleur2 = ListProperty([])
    window_size = ListProperty([])

    def __init__(self, **kwargs):
        super(MyPaintWidget, self).__init__(**kwargs)
        self.palette = MyPaintPalette()
        self.window_size = Window.size
        Window.bind(size = self.change_window_size)
        self.the_grid = GridLayout(cols = 2, row_force_default = True, row_default_height = 30)
        self.get_colours((1, 0, 0), (0, 1, 0), (0, 0, 1), (0, 1, 1), (1, 1, 1))
        self.add_widget(self.the_grid)
        self.add_widget(self.palette)
        #self.bind(window_size = self.on_window_size)

    def change_window_size(self, instance, value):
        self.the_grid.pos = [Window.width - 100, Window.height - 100]
        self.the_grid.canvas.clear()
        with self.the_grid.canvas:
            Color( 1, 1, 0)
            Rectangle(pos = self.the_grid.pos, size = self.the_grid.size)

    def get_colours(self, *args):
        self.the_grid.pos = [Window.width - 100, Window.height - 100]
        for arg in args:
            a_color = ColorChoice(arg)
            self.the_grid.add_widget(a_color)

    def on_touch_down(self, touch):
        la_limit = 0.25 # To not make it too dark

        #Did the player choose a diffrent color
        for arg in self.the_grid.children:
            if arg.collide_point(*touch.pos):
                self.change_color(arg)
                return

        #Is the player trying to draw over our the_grid? Don't let him
        if touch.pos[0] > (self.the_grid.pos[0]) and touch.pos[1] > (self.the_grid.y):
            print "yes"
            return

        touch.grab(self)
        if self.la_couleur2 == []:
            la_couleur = random(), random(), random()

            #while the color is too dark change it
            while (la_couleur[0] <  la_limit or la_couleur[1] < la_limit or la_couleur[2] < la_limit):
                la_couleur = random(), random(), random()

        with self.palette.canvas:

            if self.la_couleur2 == []:
                Color(*(la_couleur))
            else:
                Color(*(self.la_couleur2))
            d = 30.0
            Ellipse(pos = (touch.x - d / 2, touch.y - d / 2), size = (d, d))
            touch.ud['line'] = Line(points = (touch.x, touch.y))

    def change_color(self, the_color_widget):
        if the_color_widget.color != [1, 1, 1]:  # When the color is white go back to choosing random colors
            self.la_couleur2 = the_color_widget.color
        else:
            self.la_couleur2 = []


    def on_touch_move(self, touch):
        if touch.grab_current is self:
            #Is the player trying to draw over our grid?
            if self.the_grid.collide_point(*touch.pos):
                return
            touch.ud['line'].points += [touch.x, touch.y]



class MyPaintApp(App):
    def build(self):
        parent = Widget()
        the_painter = MyPaintWidget()
        clear_button = Button(text = "Clear")
        clear_button.size = [50, 50]

        def clear_stuff(obj):
            the_painter.palette.canvas.clear()

        clear_button.bind(on_release = clear_stuff)
        parent.add_widget(clear_button)
        parent.add_widget(the_painter)
        return parent

if __name__ == "__main__":
    MyPaintApp().run()



