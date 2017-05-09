from __future__ import absolute_import 

import sys
import octoprint.plugin
import paho.mqtt.client as mqtt
import octoprint.printer


class Julia3GMQTT(octoprint.plugin.StartupPlugin):
	def show_connect_info(self,client,userdata,flags,rc):
		self._logger.info("Connected to " + str(self.url))

	def show_message(self, client, userdata, message):
		msg=str(message.payload)
		topic=str(message.topic)
		self._logger.info(topic + " : " + msg)
		try:
			if topic == "octoprint/plugin/mqtt_test/operation":
				if msg == "pause":
					self.juliaPrinter.pause_print()
				if msg == "start":
					self.juliaPrinter.start_print()
				if msg == "stop":
					self.juliaPrinter.stop_print()
			if topic == "octoprint/plugin/mqtt_test/testaxes":
				if msg == "movex":
					self._logger.info("Moving X")
					self.juliaPrinter.jog(dict(x=0.05))
				if msg == "movey":
					self._logger.info("Moving Y")
					self.juliaPrinter.jog(dict(y=0.05))
				if msg == "movez":
					self._logger.info("Moving Z")
					self.juliaPrinter.jog(dict(z=0.05))
		except:
			self._logger.info(sys.exc_info()[0])
	def disconnect(self):
		self._logger.info("MQTT Broker Disconnected")
	def __init__(self):
		self.url="test.mosquitto.org" #self._settings.get(["broker","url"])	
		self.port=1883  #self._settings.get(["broker","port"])
		self.julia=mqtt.Client("Julia3G")
		self.julia.on_connect=self.show_connect_info
		self.julia.on_message=self.show_message
		self.julia.on_disconnect=self.disconnect


	def on_after_startup(self):
		self.juliaPrinter=self._printer

		
		self.julia.connect(self.url,self.port)

		self.julia.loop_start()
		#Subscribe to a list of plugins here
		#Testing start, stop, pause for now
		self.julia.subscribe("octoprint/plugin/mqtt_test/operation")
		self.julia.subscribe("octoprint/plugin/mqtt_test/testaxes")
	def show_connect_info(self,client,userdata,flags,rc):
		self._logger.info("Connected to " + str(self.url))

	def on_message(client1, userdata, message):
		print(str(message.payload))
	def __del__(self):
		self.julia.disconnect()
		self.julia.loop_stop()

	

__plugin_implementations__ = [Julia3GMQTT()]
