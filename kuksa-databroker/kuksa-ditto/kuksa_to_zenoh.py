import asyncio
import json
import time
import zenoh
import random
from kuksa_client.grpc.aio import VSSClient

THING_ID = "my-vehicle"
ZENOH_KEY = f"vehicle/{THING_ID}/telemetry"

MIN_DELAY = 0.5
MAX_DELAY = 3

MISSING_SIGNAL_CHANCE = 0.15
OMITTABLE_FIELDS = [
    "vehicleSpeed",
    "engineSpeed",
    "throttlePosition",
    "coolantTemperature",
    "batteryHealth"
]

async def main():
    with zenoh.open(zenoh.Config()) as session:
        pub = session.declare_publisher(ZENOH_KEY)

        async with VSSClient("127.0.0.1", 55556) as client:
            while True:
                values = await client.get_current_values([
                    "Vehicle.OBD.VehicleSpeed",
                    "Vehicle.OBD.CoolantTemperature",
                    "Vehicle.OBD.ThrottlePosition",
                    "Vehicle.OBD.EngineSpeed",
                    "Vehicle.OBD.BatteryHealth"
                ])

                payload = {
                    "vehicleSpeed": values["Vehicle.OBD.VehicleSpeed"].value,
                    "engineSpeed": values["Vehicle.OBD.EngineSpeed"].value,
                    "throttlePosition": values["Vehicle.OBD.ThrottlePosition"].value,
                    "coolantTemperature": values["Vehicle.OBD.CoolantTemperature"].value,
                    "batteryHealth": values["Vehicle.OBD.BatteryHealth"].value,
                    "timestamp": int(time.time())
                }

                is_valid = (
                    0 <= payload["vehicleSpeed"] <= 255 and
                    0 <= payload["engineSpeed"] <= 1000 and
                    0 <= payload["throttlePosition"] <= 200 and
                    0 <= payload["coolantTemperature"] <= 500 and
                    0 <= payload["batteryHealth"] <= 100
                )

                if not is_valid:
                    print("Invalid data filtered out:", payload)
                    await asyncio.sleep(1)
                    continue

                if random.random() < MISSING_SIGNAL_CHANCE:
                    missing_field = random.choice(OMITTABLE_FIELDS)
                    del payload[missing_field]
                    print(f"Missing-signal simulation: omitted {missing_field}")

                delay_seconds = random.uniform(MIN_DELAY, MAX_DELAY)
                print(f"Applying dynamic delay: {delay_seconds:.2f} seconds")
                await asyncio.sleep(delay_seconds)

                print("Publishing to Zenoh:", payload)
                pub.put(json.dumps(payload))
                await asyncio.sleep(1)

asyncio.run(main())