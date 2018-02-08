# import mqttPublisher as mP
# from time import sleep

# def coffeeSizeFunction(keyword):
# 	if (keyword == "latte"):
# 		# Might be useful to first check if the coffee machine is already off,
# 		#	or in the middle of brewing. 
# 		payload = "Size LATTE"
# 		mP.mqtt_client.loop_start()
# 		#sleep(0.1)
# 		mP.mqtt_client.publish("PicroftCoffee-Policy", payload, qos=1)
# 		print ("sent: " + payload)
# 		mP.mqtt_client.loop_stop()

# 	elif (keyword == "cappuccino"):
# 		# Send message to turn on coffee
# 		payload = "Size CAPPUCCINO"
# 		mP.mqtt_client.loop_start()
# 		#sleep(0.1)
# 		mP.mqtt_client.publish("PicroftCoffee-Policy", payload, qos=1)
# 		print ("sent: " + payload)
# 		mP.mqtt_client.loop_stop()

# 	elif (keyword == "regular"):
# 		# Send message to turn on coffee
# 		payload = "Size REGULAR"
# 		mP.mqtt_client.loop_start()
# 		#sleep(0.1)
# 		mP.mqtt_client.publish("PicroftCoffee-Policy", payload, qos=1)
# 		print ("sent: " + payload)
# 		mP.mqtt_client.loop_stop()
		
# 	elif (keyword == "coffee"):
# 		# Send message to turn on coffee
# 		payload = "Size REGULAR"
# 		mP.mqtt_client.loop_start()
# 		#sleep(0.1)
# 		mP.mqtt_client.publish("PicroftCoffee-Policy", payload, qos=1)
# 		print ("sent: " + payload)
# 		mP.mqtt_client.loop_stop()
