import kivy
from math import sin
from bluetooth import *
from kivy.app import App
from kivy.uix.tabbedpanel import TabbedPanel
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.popup import Popup
from kivy.uix.button import Button
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.stacklayout import StackLayout
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.lang import Builder
from kivy.properties import ObjectProperty, StringProperty
from kivy.garden.graph import Graph, MeshLinePlot
from kivy.clock import Clock

kivy.require('1.8.0')

Builder.load_string("""

<Dashboard>:
	size_hint: 1, 1
	pos_hint: {'center_x': .5, 'center_y': .5}
	tab_pos: 'bottom_left'
	do_default_tab: False

	TabbedPanelItem:
		text: 'Nav'
		Label:
			text: 'Nav system goes here'
	TabbedPanelItem:
		text: 'Status'
		Label:
			text: 'Performance, health, and eco stats go here'
		<Performance>:

	TabbedPanelItem:
		text: 'Media'
		BoxLayout:
			orientation: 'horizontal'
			text: 'Media'
			Label:
				text: 'A field!'
				size_hint: 0.1, 0.1
				pos_hint: {'center_x': 0.5, 'center_y': 0.5}
			BoxLayout:
				orientation: 'vertical'
				size_hint: 0.1, 1
				Label:
					size_hint: 1, 0.1
				Label:
					text: 'Song Name'
					font_size: 30
					size_hint: 1, 0.1
					halign: 'left'
					valign: 'bottom'
					pos_hint: {'center_x': 0.2, 'center_y': 0.5}
				Label:
					text: 'Artist Name'
					font_size: 20
					size_hint: 1, 0.2
					halign: 'left'
					valign:'top'
					pos_hint: {'center_x': 0.15, 'center_y': 0.5}
				Label:
					size_hint: 1, 0.05
				Image:
					source: 'brawl.jpg'
				Label:
					size_hint: 1, 0.1
				BoxLayout:
					orientation: 'horizontal'
					size_hint: 1, 0.3
					Label:
						size_hint: 1, 1
					Button:
						text: 'RWND'
						pos_hint: {'center_x': 0.5, 'center_y': 0.5}
						on_press: app.mplayer.rewind()
					Label:
						size_hint: 0.3, 1
					Button:
						text: 'Play'
						pos_hint: {'center_x': 0.5, 'center_y': 0.5}
						on_press: app.mplayer.play_song()
					Label:
						size_hint: 0.3, 1
					Button:
						text: 'FFWD'
						pos_hint: {'center_x': 0.5, 'center_y': 0.5}
						on_press: app.mplayer.fast_forward()
					Label:
						size_hint: 1, 1
				Label:
					size_hint: 1, 0.1
	Button:
		text: 'Hello'

""")

class Performance(Widget):
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

class Dashboard(TabbedPanel):
	pass

class MusicPlayer():
	def play_song(x):
		print "Playing song!"
	def fast_forward(x):
		print "Skipping forward!"
	def rewind(x):
		print "Skipping back!"

class Dash(App):
	mplayer = MusicPlayer()

	def build(self):
		parent = Dashboard()
		parent.add_widget(Performance)
		return Dashboard()


if __name__ == '__main__':
	Dash().run()