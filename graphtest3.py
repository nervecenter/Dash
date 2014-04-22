from bluetooth import *
from kivy.uix.popup import Popup
from kivy.uix.button import Button
from kivy.uix.togglebutton import ToggleButton
import kivy

from math import sin
from bluetooth import *
kivy.require('1.8.0')

from kivy.uix.stacklayout import StackLayout
from kivy.uix.widget import Widget
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.label import Label
from kivy.properties import ObjectProperty, StringProperty
from kivy.app import App
from kivy.garden.graph import Graph, MeshLinePlot
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.clock import Clock

class PerformanceApp(App):
    ###Tristan's bluetooth module for receiving

    #port = 0x1001
    #backlog = 1

    #server_sock=BluetoothSocket( L2CAP )
    #server_sock.bind(("",port))
    #print 'listening'
    #server_sock.listen(1)
    #print "Found"
    #client_sock,address = server_sock.accept()
    #print "Accepted connection from ",address, " | ", client_sock
    
    graph = Graph(xlabel='Time', ylabel='', x_ticks_minor=5,
        x_ticks_major=100, y_ticks_major=12,
        y_grid_label=True, x_grid_label=True, padding=5,
        x_grid=True, y_grid=True, xmin=-0, xmax=3000, ymin=0, ymax=120, size_hint=(.8,.8))

    RPMbtn = ToggleButton(text='RPM', size_hint=(.2,.2))
    ENGbtn = ToggleButton(text='Engine Load', size_hint=(.2,.2))
    COTbtn = ToggleButton(text='Coolant Temp', size_hint=(.2,.2))
    BCKbtn = ToggleButton(text='Back', size_hint=(.2,.2))

    RPMstate = 0
    ENGstate = 0
    COTstate = 0

    RPMlist = []
    while(len(RPMlist)<3000):
        RPMlist.append(0)   
    
    ENGlist = []
    while(len(ENGlist)<3000):
        ENGlist.append(0)

    COTlist = []
    while(len(COTlist)<3000):
        COTlist.append(0)

    
    def build(self):
        
        layout = StackLayout()
        layout.add_widget(self.RPMbtn)
        layout.add_widget(self.ENGbtn)
        layout.add_widget(self.COTbtn)
        layout.add_widget(self.BCKbtn)
        layout.add_widget(self.graph)

        self.RPMbtn.bind(on_press = self.RPMplot)
        self.ENGbtn.bind(on_press = self.ENGplot)
        self.COTbtn.bind(on_press = self.COTplot)

        Clock.schedule_interval(self.updateUI, 1.0/60.0)
        return layout

    def RPMplot(self, RPMbtn):
        if (self.RPMstate == 0):
            self.RPMstate = 1
        else:
            self.RPMstate = 0
            
    def ENGplot(self, ENGbtn):
        if (self.ENGstate == 0):
            self.ENGstate = 1
        else:
            self.ENGstate = 0
            
    def COTplot(self, COTbtn):
        if (self.COTstate == 0):
            self.COTstate = 1
        else:
            self.COTstate = 0
        
    
    def updateUI(self, dt):
        try:
            self.graph.remove_plot(plot1)
        except:
            pass
        try:
            self.graph.remove_plot(plot2)
        except:
            pass
        try:
            self.graph.remove_plot(plot3)
        except:
            pass
        
        data = "0:00:04.990896,843,28,37"#client_sock.recv(1024)   ###receive data as a string into 'data'
        values = data.split(',')
        
        self.RPMlist.insert(0, int(values[1])/100)
        if(len(self.RPMlist)>3000):
            self.RPMlist = self.RPMlist[:3000]

        self.ENGlist.insert(0, int(values[2]))
        if(len(self.ENGlist)>3000):
            self.ENGlist = self.ENGlist[:3000]

        self.COTlist.insert(0, int(values[3]))
        if(len(self.COTlist)>3000):
            self.COTlist = self.COTlist[:3000]
        
        self.RPMbtn.text = str('RPM: ' + values[1])
        self.ENGbtn.text = str('Engine Load: ' + values[2])
        self.COTbtn.text = str('Coolant Temp: ' + values[3])

        self.RPMlist.reverse()
        self.ENGlist.reverse()
        self.COTlist.reverse()

        if(self.RPMstate == 1):
            plot1 = MeshLinePlot(color=[1, 0, 0, 1])
            plot1.points = ((x, self.RPMlist[x]) for x in xrange(0,3000))
            self.graph.add_plot(plot1)
        
        if(self.ENGstate == 1):
            plot2 = MeshLinePlot(color=[0, 1, 0, 1])
            plot2.points = ((x, self.ENGlist[x]) for x in xrange(0,3000))
            self.graph.add_plot(plot2)

        if(self.COTstate == 1):
            plot3 = MeshLinePlot(color=[0, 0, 1, 1])
            plot3.points = ((x, self.COTlist[x]) for x in xrange(0,3000))
            self.graph.add_plot(plot3)

        self.RPMlist.reverse()
        self.ENGlist.reverse()
        self.COTlist.reverse()


PerformanceApp().run()
