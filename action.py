
# import mqttPublisher as mP
# from time import sleep


# def actionFunction(keyword, coffeeType):
# 	if (action == "brew") or (action == "make"):
# 		# Change state to BREWING
# 		# Turn on an LED
# 		# Publish message over mqtt to turn on LED
# 		payload = "State BREW " + coffeeType
# 		mP.mqtt_client.loop_start()
# 		sleep(0.1)
# 		mP.mqtt_client.publish("PicroftCoffee-Policy", payload, qos=1)
# 		#print ("sent: " + payload)
# 		mP.mqtt_client.loop_stop()
		
# 	elif (action == "cancel") or (action == "stop"):
# 		# Change state to NOT_BUSY
# 		# Publish message to turn off LED
# 		payload = "State WAIT " + coffeeType
# 		mP.mqtt_client.loop_start()
# 		sleep(0.1)
# 		mP.mqtt_client.publish("PicroftCoffee-Policy", payload, qos=1)
# 		#print ("sent: " + payload)
# 		mP.mqtt_client.loop_stop()