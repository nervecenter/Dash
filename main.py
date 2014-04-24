'''
Created on Feb 26, 2014

@author: Ian Milanian

./build.py --package com.kivy.dash --name Dash --version 1.0 --dir /home/kivy/Documents/dash_project \
           --permission INTERNET \
           --permission WRITE_EXTERNAL_STORAGE \
           --permission ACCESS_FINE_LOCATION \
           --permission ACCESS_COARSE_LOCATION \
           debug installd

'''

import kivy
kivy.require('1.0.7')

from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.properties import StringProperty
from MapViewer import MapViewer
from kivy.lang import Builder
from plyer import gps

kv = '''
BoxLayout:
    orientation: 'vertical'

    Label:
        text: app.gps_location

    Label:
        text: app.gps_status

    BoxLayout:
        size_hint_y: None
        height: '48dp'
        padding: '4dp'

        ToggleButton:
            text: 'Start' if self.state == 'normal' else 'Stop'
            on_state: app.gps.start() if self.state == 'down' else app.gps.stop()
'''


class KVMaps(App):

#     gps_location = StringProperty()
#     gps_status = StringProperty('Click Start to get GPS location updates')
  
    def build(self):
#         self.gps = gps
#         try:
#             self.gps.configure(on_location=self.on_location,
#                     on_status=self.on_status)
#         except NotImplementedError:
#             import traceback; traceback.print_exc()
#             self.gps_status = 'GPS is not implemented for your platform'
#  
#         return Builder.load_string(kv)
      
        layout = FloatLayout()
        self.mv = MapViewer(maptype="satellite", provider="bing")
        
        #self.mv.move_to(28.1403873167, 82.34676305, 5)

        layout.add_widget(self.mv)
        return layout

# #    @mainthread
#     def on_location(self, **kwargs):
#         self.gps_location = '\n'.join([
#              '{}={}'.format(k, v) for k, v in kwargs.items()])
#  
# #    @mainthread
#     def on_status(self, stype, status):
#         self.gps_status = 'type={}\n{}'.format(stype, status)

if __name__ in ('__android__','__main__'):
  KVMaps().run()