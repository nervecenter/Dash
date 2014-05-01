# dash.py
# Python Dashboard Team
# Tristan Hook, David Drew, Arian Milanian, Zach Sutherland, Chris Collazo

import kivy
import random
kivy.require('1.7.0')

from bluetooth import *
from kivy.app import App
from kivy.garden.graph import Graph, MeshLinePlot
from MapViewer import MapViewer
from plyer import gps
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.properties import StringProperty
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.uix.tabbedpanel import TabbedPanel, TabbedPanelHeader
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.stacklayout import StackLayout
from kivy.uix.filechooser import FileChooserListView
from kivy.uix.togglebutton import ToggleButton
from kivy.lang import Builder

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

class Performance(StackLayout):
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
    
    def __init__(self, **kwargs):
        """Creates the layout and widget tree for performance class"""
        super(Performance, self).__init__(**kwargs)
        self.add_widget(self.RPMbtn)
        self.add_widget(self.ENGbtn)
        self.add_widget(self.COTbtn)
        self.add_widget(self.graph)

        self.RPMbtn.bind(on_press = self.RPMplot)
        self.ENGbtn.bind(on_press = self.ENGplot)
        self.COTbtn.bind(on_press = self.COTplot)

        Clock.schedule_interval(self.updateUI, 1.0/10.0)
        ## pings the updateUI function ten times a second, giving
        ## the graph a framerate of 10fps

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
        
        # try:
        #     data = client_sock.recv(1024)

        #     if (len(data) < 1):
        #         data = self.last_data
        #     else:
        #         print data

        #     self.last_data = data

        ## Receive data as a string into 'data'. If the
        ## socket produces no information, as the vehicle will
        ## typically vary on how long between data is sent
        ## the data will either get '0,0,0,0' indicating no data
        ## has been sent yet, or it will use the last good data received
            
        # except IOError, NameError:
        #     data = last_data
            
        # if (client_sock == False):
        #     print "Socket Connection Lost"
            
        # values = data.split(',')

        ## data is split into
        
        self.RPMlist.insert(0, random.randint(60,80))
        if(len(self.RPMlist)>300):
             self.RPMlist = self.RPMlist[:300]
        
        self.ENGlist.insert(0, random.randint(20,40))
        if(len(self.ENGlist)>300):
             self.ENGlist = self.ENGlist[:300]
        
        self.COTlist.insert(0, random.randint(1,30))
        if(len(self.COTlist)>300):
             self.COTlist = self.COTlist[:300]
        
        # Used for testing random numbers in the graph
        
        
        # self.RPMlist.insert(0, int(values[1])/100)
        # if(len(self.RPMlist)>300):
        #     self.RPMlist = self.RPMlist[:300]

        # self.ENGlist.insert(0, int(values[2]))
        # if(len(self.ENGlist)>300):
        #     self.ENGlist = self.ENGlist[:300]

        # self.COTlist.insert(0, int(values[3]))
        # if(len(self.COTlist)>300):
        #     self.COTlist = self.COTlist[:300]

        ## The values (data) are inserted into their respective
        ## performance metric lists
        
		self.RPMbtn.text = str('RPM: ' + str(self.RPMlist[0]))
		self.ENGbtn.text = str('Engine Load: ' + str(self.ENGlist[0]))
		self.COTbtn.text = str('Coolant Temp: ' + str(self.COTlist[0]))
		
		## Used to place random numbers in graph for testing

        # self.RPMbtn.text = str('RPM: ' + values[1])
        # self.ENGbtn.text = str('Engine Load: ' + values[2])
        # self.COTbtn.text = str('Coolant Temp: ' + values[3])

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

class MusicPlayer(BoxLayout):
    '''
    This class initializes and implements our music player UI layout.
    '''
	def __init__(self, **kwargs):
		super(MusicPlayer, self).__init__(**kwargs)
        # Implement music player in two horizontal panes
		self.orientation = 'horizontal'

        # This column is our file manager, uses basic
        # Kivy file manager for now
		fileMan = BoxLayout(orientation='vertical',
							pos_hint={'center_x': 0.5,'center_y': 0.5}, 
							size_hint=(0.1, 1),
							padding=(1,1))
		fileManPlaceholder = FileChooserListView()
		fileMan.add_widget(fileManPlaceholder)

        # This is the column for our player, containing
        # song name, album art, playback controls. Labels
        # are used to pad space, since we don't have a
        # drag 'n drop editor.
		player = BoxLayout(orientation='vertical',
						   size_hint=(0.1,1))
		player.add_widget(Label(size_hint=(1, 0.1)))
		songName = Label(text='Snow (Hey Oh)',
						 font_size=30,
						 size_hint=(1,0.1),
						 halign='left',
						 valign='bottom',
						 pos_hint={'center_x':0.3,'center_y':0.5})
		player.add_widget(songName)
		artistName = Label(text='Red Hot Chili Peppers',
						   font_size=20,
						   size_hint=(1,0.2),
						   halign='left',
						   valign='top',
						   pos_hint={'center_x':0.3,'center_y':0.5})
		player.add_widget(artistName)
		player.add_widget(Label(size_hint=(1, 0.05)))
		player.add_widget(Image(source='graphics/arcadium.jpg'))

		player.add_widget(Label(size_hint=(1, 0.1)))
		
		playBackButtons = BoxLayout(orientation='horizontal',
									size_hint=(1,0.24))
		playBackButtons.add_widget(Label(size_hint=(1,1)))
		
		rewind = Button(background_normal='graphics/rewindbutton.png',
						pos_hint={'center_x':0.5,'center_y':0.5})
		#rewind.bind(on_press=rewind())
		playBackButtons.add_widget(rewind)
		playBackButtons.add_widget(Label(size_hint=(0.3,1)))
		
		play = Button(background_normal='graphics/playbutton.png',
					  pos_hint={'center_x':0.5,'center_y':0.5})
		#play.bind(on_press=play_song())
		playBackButtons.add_widget(play)
		playBackButtons.add_widget(Label(size_hint=(0.3,1)))
		
		ffwd = Button(background_normal='graphics/fastforwardbutton.png',
					  pos_hint={'center_x':0.5,'center_y':0.5})
		#ffwd.bind(on_press=fast_forward())
		playBackButtons.add_widget(ffwd)
		
		playBackButtons.add_widget(Label(size_hint=(1,1)))
		player.add_widget(playBackButtons)

		player.add_widget(Label(size_hint=(1,0.1)))

		self.add_widget(fileMan)
		self.add_widget(player)
	
    # Playback buttons print to console for now,
    # since Python media playback support is iffy.	
	def play_song(self):
        '''Plays a given song.'''
		print "Playing song!"
	def fast_forward(self):
        '''Fast-forwards the playing song.'''
		print "Skipping forward!"
	def rewind(self):
        '''Rewings the playing song.'''
		print "Skipping back!"

class KVMaps(FloatLayout, App):
	def __init__(self, **kwargs):
		super(KVMaps, self).__init__(**kwargs)
		mv = MapViewer(maptype="satellite", provider="bing")
		self.add_widget(mv)

		box = BoxLayout(orientation='vertical')
		box.add_widget(Label(text=app.gps_location))
		box.add_widget(Label(text=app.gps_status))
		toggle = BoxLayout(size_hint_y: None,
						   height='48dp',
						   padding='4dp')
		toggle.add_widget(ToggleButton(text='Start' if self.state == 'normal' else 'Stop',
									   on_state=app.gps.start() if self.state == 'down' else app.gps.stop()))
		box.add_widget(toggle)
		self.add_widget(box)

class Dash(App):
	def build(self):
        # App is built as a tabbed panel with three tabs:
        # Navigation, Status, and Media. These allow quick
        # access to the things you actually want to do in
        # a car without excessive UI navigation.
		tp = TabbedPanel()
		tp.do_default_tab = False
		tp.tab_pos = 'bottom_mid'
		tp.tab_width = Window.width / 3

		nav = TabbedPanelHeader(text='Nav')
		status = TabbedPanelHeader(text='Status')
		media = TabbedPanelHeader(text='Media')
		
		tp.add_widget(nav)
		tp.add_widget(status)
		tp.add_widget(media)

		#nav.content = Label(text = 'Nav system goes here')
		#status.content = Label(text = 'Performance, health, and eco stats go here')
		#media.content = Label(text = 'Media player goes here')

        # Each tab's content is implemented in a tab above.
		nav.content = KVMaps()
		status.content = Performance()
		media.content = MusicPlayer()
		return tp

	def on_location(self, **kwargs):
        self.gps_location = '\n'.join([
             '{}={}'.format(k, v) for k, v in kwargs.items()])
    def on_status(self, stype, status):
        self.gps_status = 'type={}\n{}'.format(stype, status)

if __name__ == '__main__':
	Dash().run()