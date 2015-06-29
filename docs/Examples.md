
# RPM Logger

```python

import obd


def main():

	# connect to the car
	connection = obd.OBD()

	# handles connection errors
	if not connection.is_connected():
		print("Failed to connect")
		return

	# open the output file
	with open("rpm.txt", "w") as f:

		# loop indefinitely
		while True:

			# read the car's RPM
			r = connection.query(obd.commands.RPM)

			if not r.is_null():
				# write CSV "time, RPM" to the log file
				f.write("%d, %d" % (r.time, r.value)) 


if __name__ == "__main__":
	main()

```

<br>

# Async RPM Logger

```python

import obd
import time


log_file = None

# callback fired on every new RPM response
def on_RPM(r):
	if not r.is_null():
		# write CSV "time, RPM" to the log file
		log_file.write("%d, %d" % (r.time, r.value)) 


def main():
	global log_file

	# connect to the car
	connection = obd.Async()

	# handles connection errors
	if not connection.is_connected():
		print("Failed to connect")
		return

	# listen to the car's RPM, and subscribe the callback
	connection.watch(obd.commands.RPM, callback=on_RPM)

	# open the output file
	with open("rpm.txt", "w") as f:
		
		log_file = f

		# begin data collection
		connection.start()
		
		# record for 10 seconds
		time.sleep(10)

		# stop recording
		connection.stop()



if __name__ == "__main__":
	main()

```

---

<br>
