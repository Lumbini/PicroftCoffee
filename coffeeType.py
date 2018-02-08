# import mqttPublisher as mP
# from time import sleep

# def coffeeTypeFunction(keyword):
# 	if (keyword == "small"):
# 		# Might be useful to first check if the coffee machine is already off,
# 		#	or in the middle of brewing. 
# 		payload = "Size SMALL"
# 		mP.mqtt_client.loop_start()
# 		#sleep(0.1)
# 		mP.mqtt_client.publish("PicroftCoffee-Policy", payload, qos=1)
# 		print ("sent: " + payload)
# 		mP.mqtt_client.loop_stop()

# 	elif (keyword == "medium"):
# 		# Send message to turn on coffee
# 		payload = "Size MEDIUM"
# 		mP.mqtt_client.loop_start()
# 		#sleep(0.1)
# 		mP.mqtt_client.publish("PicroftCoffee-Policy", payload, qos=1)
# 		print ("sent: " + payload)
# 		mP.mqtt_client.loop_stop()
		
# 	elif (keyword == "large"):
# 		# Send message to turn on coffee
# 		payload = "Size LARGE"
# 		mP.mqtt_client.loop_start()
# 		#sleep(0.1)
# 		mP.mqtt_client.publish("PicroftCoffee-Policy", payload, qos=1)
# 		print ("sent: " + payload)
# 		mP.mqtt_client.loop_stop()
