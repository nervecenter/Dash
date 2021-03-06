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

server_sock=BluetoothSocket( RFCOMM )
server_sock.bind(("",port))
print 'listening'
server_sock.listen(1)
print "Found"
client_sock,address = server_sock.accept()
print "Accepted connection from ",address, " | ", client_sock
client_sock.settimeout(0)

## creates and accepts the initial bluetooth connection
## sets a timeout on the client_sock socket, which is typically a
## blocking connection. This stops the program from hanging when
## receiving the data

class PerformanceApp(App):
    """
    This class contains the graphing application for the Kivy Dashboard
    Application. It accepts a buffer string from a socket connection
    established elsewhere in the software, then parses the data to be
    inserted into a graph"""
    graph = Graph(xlabel='Time', ylabel='', x_ticks_minor=5,
        x_ticks_major=100, y_ticks_major=12,
        y_grid_label=True, x_grid_label=True, padding=5,
        x_grid=True, y_grid=True, xmin=-0, xmax=300, ymin=0, ymax=120, size_hint=(1,.9))

    ## creates graph object to be accessed by updateUI function

    plot1 = MeshLinePlot(color=[1, 0, 0, 1])
    plot2 = MeshLinePlot(color=[0, 1, 0, 1])
    plot3 = MeshLinePlot(color=[0, 0, 1, 1])

    last_data = '0,0,0,0'
    ## creates the initial plot objects for the garden.graph function
    ## with defining color

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
    ## Creates three lists, of length 300, all initialized to zero
    ## The graph will build from this list, and if it is not initialized to
    ## zero beforehand, it will get an indexing error
    
    def build(self):
        """Creates the layout and widget tree for performance class"""
        layout = StackLayout()
        layout.add_widget(self.RPMbtn)
        layout.add_widget(self.ENGbtn)
        layout.add_widget(self.COTbtn)
        layout.add_widget(self.graph)

        self.RPMbtn.bind(on_press = self.RPMplot)
        self.ENGbtn.bind(on_press = self.ENGplot)
        self.COTbtn.bind(on_press = self.COTplot)

        Clock.schedule_interval(self.updateUI, 1.0/10.0)
        ## pings the updateUI function ten times a second, giving
        ## the graph a framerate of 10fps
        return layout

    def RPMplot(self, RPMbtn):
        """sets the state for the RPM button widget"""
        if (self.RPMstate == 0):
            self.RPMstate = 1
        else:
            self.RPMstate = 0
            
    def ENGplot(self, ENGbtn):
        """sets the state for the Engine Load button widget"""
        if (self.ENGstate == 0):
            self.ENGstate = 1
        else:
            self.ENGstate = 0
            
    def COTplot(self, COTbtn):
        """sets the state for the Coolant Temp button widget"""
        if (self.COTstate == 0):
            self.COTstate = 1
        else:
            self.COTstate = 0
        
    
    def updateUI(self, dt):
        """Updates the parameters of the graph.

        This function will remove redundant plots on the graph
        then receive new data from bluetooth socket.
        The data is broken up and placed on the graph
        depending on the state of the button widgets
        """
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
        ## tries to remove the previously added plots to the graph
        ## this prevents ghosting on the graph itself
        
        try:
            data = client_sock.recv(1024)

            if (len(data) < 1):
                data = self.last_data
            else:
                print data

            self.last_data = data

        ## Receive data as a string into 'data'. If the
        ## socket produces no information, as the vehicle will
        ## typically vary on how long between data is sent
        ## the data will either get '0,0,0,0' indicating no data
        ## has been sent yet, or it will use the last good data received
            
        except IOError, NameError:
            data = last_data
            
        if (client_sock == False):
            print "Socket Connection Lost"
            
        values = data.split(',')
        ## data is split into
        
        ##self.RPMlist.insert(0, random.randint(60,80))
        ##if(len(self.RPMlist)>300):
        ##      self.RPMlist = self.RPMlist[:300]
        ##
        ##self.ENGlist.insert(0, random.randint(20,40))
        ##if(len(self.ENGlist)>300):
        ##      self.ENGlist = self.ENGlist[:300]
        ##
        ##self.COTlist.insert(0, random.randint(1,30))
        ##if(len(self.COTlist)>300):
        ##      self.COTlist = self.COTlist[:300]
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

        ## The values (data) are inserted into their respective
        ## performance metric lists
        
##        self.RPMbtn.text = str('RPM: ' + str(self.RPMlist[0]))
##        self.ENGbtn.text = str('Engine Load: ' + str(self.ENGlist[0]))
##        self.COTbtn.text = str('Coolant Temp: ' + str(self.COTlist[0]))
##
## Used to place random numbers in graph for testing
##

        self.RPMbtn.text = str('RPM: ' + values[1])
        self.ENGbtn.text = str('Engine Load: ' + values[2])
        self.COTbtn.text = str('Coolant Temp: ' + values[3])

        ## Updates the buttons on screen to the correct values

        self.RPMlist.reverse()
        self.ENGlist.reverse()
        self.COTlist.reverse()

        ## Reverses each list so that the graph is displayed as scrolling from
        ## the right, rather than the left

        if(self.RPMstate == 1):
            self.plot1.points = ((x, self.RPMlist[x]) for x in xrange(0,300))
            self.graph.add_plot(self.plot1)
        
        if(self.ENGstate == 1):
            self.plot2.points = ((x, self.ENGlist[x]) for x in xrange(0,300))
            self.graph.add_plot(self.plot2)
    
        if(self.COTstate == 1):
            self.plot3.points = ((x, self.COTlist[x]) for x in xrange(0,300))
            self.graph.add_plot(self.plot3)

        ## The App checks the state of the buttons, and updates the graph
        ## if the buttons are toggled
        
        self.RPMlist.reverse()
        self.ENGlist.reverse()
        self.COTlist.reverse()

        ## Reverses the list again for correct data parsing
        
PerformanceApp().run()

