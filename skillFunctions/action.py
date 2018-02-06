
def actionFunction(action):
	if (action == "brew") or (action == "make"):
		coffeeStart()
	elif (action == "cancel") or (action == "stop"):
		coffeeStop()


def coffeeStart():
	# Change state to BREWING
	# Turn on an LED
	# Publish message over mqtt to turn on LED
	global publish_flag
	publish_flag = True




def coffeeStop():
	# Change state to NOT_BUSY
	# Publish message to turn off LED
