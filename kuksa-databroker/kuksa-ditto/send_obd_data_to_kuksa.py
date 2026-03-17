import random
import time
import asyncio
from kuksa_client.grpc.aio import VSSClient
from kuksa_client.grpc import Datapoint

battery_health = 100

# Asynchronous main function to connect to Kuksa Databroker and retrieve OBD data
async def main():
    
	# Establish an asynchronous connection to the Kuksa Databroker at the IP: 127.0.0.1 and port 55555
	async with VSSClient('127.0.0.1' , 55556) as client:

    	# Repeat Infinitely
		while True:
        	# Generate random values for each feature with the defined ranges
			VehicleSpeed = random.randint(0,255)
			EngineSpeed = random.randint(0,1000)
			ThrottlePosition = random.randint(0,200)
			CoolantTemperature = random.randint(0,500)

			global battery_health
			battery_health -= random.uniform(0.01, 0.05)
			if battery_health < 0:
				battery_health = 0

			if random.random() < 0.05:
				fault = random.choice(["speed", "engine", "throttle", "coolant"])
				if fault == "speed":
					VehicleSpeed = -20
				elif fault == "engine":
					EngineSpeed = -20
				elif fault == "throttle":
					ThrottlePosition = -20
				elif fault == "coolant":
					CoolantTemperature = -20
        
        	# Send the generated values to the Kuksa Databroker with the
        	# corresponding vehicle data paths using the 'set_current_values' function
			values = await client.set_current_values({
            	'Vehicle.OBD.VehicleSpeed' : Datapoint(VehicleSpeed),
            	'Vehicle.OBD.CoolantTemperature': Datapoint(CoolantTemperature),
            	'Vehicle.OBD.ThrottlePosition':Datapoint(ThrottlePosition),
            	'Vehicle.OBD.EngineSpeed' : Datapoint(EngineSpeed),
            	'Vehicle.OBD.BatteryHealth' : Datapoint(battery_health),
        	})

        	# Print the value for each feature
			print('Vehicle Speed = ' , VehicleSpeed)
			print('Engine Speed = ' , EngineSpeed)
			print('Throttle Position = ' , ThrottlePosition)
			print('coolant Temperature = ' , CoolantTemperature)
			print('Battery Health = ', round(battery_health,2))

        	# Pause for 1 second
			time.sleep(1)

			print('-----------------------------')

# Run the main function
asyncio.run(main())