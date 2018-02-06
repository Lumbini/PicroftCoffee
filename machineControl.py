
import mqttPublisher as mP
from time import sleep

def controlFunction(keyword):
	if (keyword == "off"):
		# Might be useful to first check if the coffee machine is already off,
		#	or in the middle of brewing. 
		payload = "Power OFF"
		mP.mqtt_client.loop_start()
		#sleep(0.1)
		mP.mqtt_client.publish("PicroftCoffee-Policy", payload, qos=1)
		print ("sent: " + payload)
		mP.mqtt_client.loop_stop()
	elif (keyword == "on"):
		# Send message to turn on coffee
		payload = "Power ON"
		mP.mqtt_client.loop_start()
		#sleep(0.1)
		mP.mqtt_client.publish("PicroftCoffee-Policy", payload, qos=1)
		print ("sent: " + payload)
		mP.mqtt_client.loop_stop()

