import kivy
kivy.require('1.7.0')

from kivy.app import App
from kivy.core.window import Window
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.uix.tabbedpanel import TabbedPanel, TabbedPanelHeader
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.filechooser import FileChooserListView
from kivy.lang import Builder

class MusicPlayer(BoxLayout):
	def __init__(self, **kwargs):
		super(MusicPlayer, self).__init__(**kwargs)
		self.orientation = 'horizontal'

		fileMan = BoxLayout(orientation='vertical',
							pos_hint={'center_x': 0.5,'center_y': 0.5}, 
							size_hint=(0.1, 1),
							padding=(1,1))
		fileManPlaceholder = FileChooserListView()
		fileMan.add_widget(fileManPlaceholder)

		player = BoxLayout(orientation='vertical',
						   size_hint=(0.1,1))
		player.add_widget(Label(size_hint=(1, 0.1)))
		songName = Label(text='Song Name',
						 font_size=30,
						 size_hint=(1,0.1),
						 halign='left',
						 valign='bottom',
						 pos_hint={'center_x':0.2,'center_y':0.5})
		player.add_widget(songName)
		artistName = Label(text='Artist Name',
						   font_size=20,
						   size_hint=(1,0.2),
						   halign='left',
						   valign='top',
						   pos_hint={'center_x':0.15,'center_y':0.5})
		player.add_widget(artistName)
		player.add_widget(Label(size_hint=(1, 0.05)))
		player.add_widget(Image(source='graphics/brawl.jpg'))

		#Pad the space between album art and buttons
		player.add_widget(Label(size_hint=(1, 0.1)))
		
		# Playback buttons initialized and laid out
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

		#Pad the buttons on the bottom
		player.add_widget(Label(size_hint=(1,0.1)))

		self.add_widget(fileMan)
		self.add_widget(player)
		
	def play_song(x):
		print "Playing song!"
	def fast_forward(x):
		print "Skipping forward!"
	def rewind(x):
		print "Skipping back!"

class Dash(App):
	def build(self):
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

		nav.content = Label(text = 'Nav system goes here')
		status.content = Label(text = 'Performance, health, and eco stats go here')
		#media.content = Label(text = 'Media player goes here')

		media.content = MusicPlayer()
		return tp

if __name__ == '__main__':
	Dash().run()