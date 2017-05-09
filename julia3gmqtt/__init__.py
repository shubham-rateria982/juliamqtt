from __future__ import absolute_import 

import octoprint.plugin
import paho.mqtt.client as mqtt
import octoprint.printer
# Okay so MQTT Plugin is not working, Screw it, Going in all on my own \m/

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
			if topic == "octoprint/plugin/mqtt_test/testaxes":
				if msg == "movex":
					self._logger.info("Moving X")
					self.juliaPrinter.jog(x=0.5)
				if msg == "movey":
					self._logger.info("Moving Y")
					self.juliaPrinter.jog(y=0.5)
				if msg == "movez":
					self._logger.info("Moving Z")
					self.juliaPrinter.jog(z=0.5)
		except:
			self._logger.info("*******Printer not connected******")
	def __init__(self):
		self.url="test.mosquitto.org" #self._settings.get(["broker","url"])	
		self.port=1883  #self._settings.get(["broker","port"])
		self.julia=mqtt.Client("Julia3G")
		self.julia.on_connect=self.show_connect_info
		self.julia.on_message=self.show_message
		self.juliaPrinter=octoprint.printer.PrinterInterface()
		try:
			self.printer_connection_data=self.juliaPrinter.get_current_connection()
			print("Connection String : {0}\nPort : {1}\nBaudrate : {2}\nPrinter_Profile : {3}".format(self.printer_connection_data))
		except:
			print("*********Printer not connected*************")
		#self.julia.on_disconnect=self.disconnect


	def on_after_startup(self):
		
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
__plugin_name="juliamqtt"
__plugin_implementations__ = [Julia3GMQTT()]