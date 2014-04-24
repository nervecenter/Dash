##Author: David Drew
##Advanced Python Semester Project
##Performance Metrics with Bluetooth Integration

import kivy
import random

from bluetooth import *
kivy.require('1.8.0')

from kivy.uix.stacklayout import StackLayout
from kivy.uix.widget import Widget
from kivy.lang import Builder
from kivy.app import App
from kivy.garden.graph import Graph, MeshLinePlot
from kivy.clock import Clock
from kivy.uix.togglebutton import ToggleButton

port = 1
backlog = 1
defaultdata = '0:00:04.990896,0,0,0'

server_sock=BluetoothSocket( RFCOMM )
server_sock.bind(("",port))
print 'listening'
server_sock.listen(1)
print "Found"
client_sock,address = server_sock.accept()
print "Accepted connection from ",address, " | ", client_sock

class PerformanceApp(App):
    ###Zach/Tristan's bluetooth module for receiving

    graph = Graph(xlabel='Time', ylabel='', x_ticks_minor=5,
        x_ticks_major=100, y_ticks_major=12,
        y_grid_label=True, x_grid_label=True, padding=5,
        x_grid=True, y_grid=True, xmin=-0, xmax=300, ymin=0, ymax=120, size_hint=(1,.9))

    plot1 = MeshLinePlot(color=[1, 0, 0, 1])
    plot2 = MeshLinePlot(color=[0, 1, 0, 1])
    plot3 = MeshLinePlot(color=[0, 0, 1, 1])

    RPMbtn = ToggleButton(text='RPM', size_hint=(.33,.1))
    ENGbtn = ToggleButton(text='Engine Load', size_hint=(.33,.1))
    COTbtn = ToggleButton(text='Coolant Temp', size_hint=(.33,.1))

    RPMstate = 0
    ENGstate = 0
    COTstate = 0

    RPMlist = []
    while(len(RPMlist)<300):
        RPMlist.append(0)   
    
    ENGlist = []
    while(len(ENGlist)<300):
        ENGlist.append(0)

    COTlist = []
    while(len(COTlist)<300):
        COTlist.append(0)
    
    def build(self):
        layout = StackLayout()
        layout.add_widget(self.RPMbtn)
        layout.add_widget(self.ENGbtn)
        layout.add_widget(self.COTbtn)
        layout.add_widget(self.graph)

        self.RPMbtn.bind(on_press = self.RPMplot)
        self.ENGbtn.bind(on_press = self.ENGplot)
        self.COTbtn.bind(on_press = self.COTplot)

        Clock.schedule_interval(self.updateUI, 1.0/1.0)
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

        ###receive data as a string into 'data'
        try:
            data = client_sock.recv(512)
            if (len(data) < 1):
                data = defaultdata
            else:
                print data
            
            lastdata = data
        except IOError, NameError:
            data = lastdata

        values = data.split(',')
        
##        self.RPMlist.insert(0, random.randint(60,80))
##        if(len(self.RPMlist)>300):
##            self.RPMlist = self.RPMlist[:300]
##
##        self.ENGlist.insert(0, random.randint(20,40))
##        if(len(self.ENGlist)>300):
##            self.ENGlist = self.ENGlist[:300]
##
##        self.COTlist.insert(0, random.randint(1,30))
##        if(len(self.COTlist)>300):
##            self.COTlist = self.COTlist[:300]
##
## Used for testing random numbers in the graph
        
        
        self.RPMlist.insert(0, int(values[1])/100)
        if(len(self.RPMlist)>300):
            self.RPMlist = self.RPMlist[:300]

        self.ENGlist.insert(0, int(values[2]))
        if(len(self.ENGlist)>300):
            self.ENGlist = self.ENGlist[:300]

        self.COTlist.insert(0, int(values[3]))
        if(len(self.COTlist)>300):
            self.COTlist = self.COTlist[:300]
        
##        self.RPMbtn.text = str('RPM: ' + str(self.RPMlist[0]))
##        self.ENGbtn.text = str('Engine Load: ' + str(self.ENGlist[0]))
##        self.COTbtn.text = str('Coolant Temp: ' + str(self.COTlist[0]))
##
## Used to place random numbers in graph for testing
##

        self.RPMbtn.text = str('RPM: ' + values[1])
        self.ENGbtn.text = str('Engine Load: ' + values[2])
        self.COTbtn.text = str('Coolant Temp: ' + values[3])

        self.RPMlist.reverse()
        self.ENGlist.reverse()
        self.COTlist.reverse()

        if(self.RPMstate == 1):
            self.plot1.points = ((x, self.RPMlist[x]) for x in xrange(0,300))
            self.graph.add_plot(self.plot1)
        
        if(self.ENGstate == 1):
            self.plot2.points = ((x, self.ENGlist[x]) for x in xrange(0,300))
            self.graph.add_plot(self.plot2)
    
        if(self.COTstate == 1):
            self.plot3.points = ((x, self.COTlist[x]) for x in xrange(0,300))
            self.graph.add_plot(self.plot3)

        self.RPMlist.reverse()
        self.ENGlist.reverse()
        self.COTlist.reverse()


PerformanceApp().run()

client_sock.close()
server_sock.close()

