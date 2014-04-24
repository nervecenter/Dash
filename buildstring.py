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