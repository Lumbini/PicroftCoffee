
import mqttPublisher as mP
from time import sleep


def actionFunction(action):
	if (action == "brew") or (action == "make"):
		coffeeStart()
	elif (action == "cancel") or (action == "stop"):
		coffeeStop()
	else:
		pass

def coffeeStart():
	# Change state to BREWING
	# Turn on an LED
	# Publish message over mqtt to turn on LED
	payload = "State BREW"
	mP.mqtt_client.loop_start()
	sleep(0.1)
	mP.mqtt_client.publish("PicroftCoffee-Policy", payload, qos=1)
	print ("sent: " + payload)
	mP.mqtt_client.loop_stop()


def coffeeStop():
	# Change state to NOT_BUSY
	# Publish message to turn off LED
	payload = "State WAIT"
	mP.mqtt_client.loop_start()
	sleep(0.1)
	mP.mqtt_client.publish("PicroftCoffee-Policy", payload, qos=1)
	print ("sent: " + payload)
	mP.mqtt_client.loop_stop()
