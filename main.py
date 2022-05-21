from urllib.request import*
import ssl
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.app import App
from kivy.graphics import Color, Rectangle
from random import random as r
from functools import partial
from kivy.lang import Builder
from kivy.uix.camera import Camera
from kivy.core.image import Image
from kivy.core.window import Window
Builder.load_string('''
<LineRectangle>:
    canvas:
        Color:
            rgba: 1, 1, 1, 1
        Line:
            width: 1
            rectangle: (self.width/2 - 10, self.height/2 + 10, 20, 20)
''')

ssl._create_default_https_context = ssl._create_unverified_context
def getColorName(string):
    resource = urlopen("https://www.color-name.com/hex/"+string)
    html =  resource.read().decode(resource.headers.get_content_charset())
    k=html.index("color name is")+14
    g=""
    while True:
        g+=html[k]
        k+=1
        if html[k]=='<' or html[k]=='.':
            break
    return(g)


class LineRectangle(Widget):
    pass

class StressCanvasApp(App):

    def add_rects(self, label, wid, count, *largs):
        im=Window.screenshot()
        m=Image.load(im, keep_data=True)
        sr=0
        sg=0
        sb=0
        for i in range(391, 408):
            for j in range(296, 314):
                color = m.read_pixel(i, j)
                sr+=color[0]
                sg+=color[1]
                sb+=color[2]
        sr=int(round((sr/324)*255, 0))
        sg=int(round((sg/324)*255, 0))
        sb=int(round((sb/324)*255, 0))
        g=str(hex(sr)[2:].zfill(2))+str(hex(sg)[2:].zfill(2))+str(hex(sb)[2:].zfill(2))
        label.text=getColorName(g)
    def build(self):
        wid = Widget()
        
        label = Label(text='')

        btn_add100 = Button(text='Provjeri boju',
                            on_press=partial(self.add_rects, label, wid, 100))

    
        piss = AnchorLayout(anchor_x='center', anchor_y='center')
        cam=Camera(play=True, resolution=(1920, 1080), allow_stretch=True)
        piss.add_widget(cam)
        piss.add_widget(LineRectangle())
        
        
        layout = BoxLayout(size_hint=(1, None), height=50)
        layout.add_widget(btn_add100)
        layout.add_widget(label)

        root = BoxLayout(orientation='vertical')
        root.add_widget(piss)
        root.add_widget(layout)
        
        return root


if __name__ == '__main__':
    StressCanvasApp().run()
