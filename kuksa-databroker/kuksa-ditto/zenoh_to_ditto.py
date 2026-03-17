import json
import requests
import zenoh

thingsURL = "http://localhost:8080/api/2/things/"
auth = ("ditto", "ditto")
THING_ID = "org.ovin:my-vehicle"
ZENOH_KEY = "vehicle/my-vehicle/telemetry"

def put_feature_value(thingID, feature, value):
    url = thingsURL + thingID + "/features/" + feature + "/properties"
    headers = {"Content-Type": "application/json"}
    data = {"value": value}
    response = requests.put(url, json=data, headers=headers, auth=auth)
    return response

def get_overheat_status(coolantTemperature):
    if coolantTemperature > 130:
        return "Critical"
    elif coolantTemperature > 110:
        return "Warning"
    else:
        return "Normal"

def get_aggressive_driving_score(vehicleSpeed, engineSpeed, throttlePosition):
    score = 0

    if vehicleSpeed > 120:
        score += 35
    elif vehicleSpeed > 80:
        score += 20

    if engineSpeed > 800:
        score += 35
    elif engineSpeed > 600:
        score += 20

    if throttlePosition > 150:
        score += 30
    elif throttlePosition > 100:
        score += 15

    if score > 100:
        score = 100

    return score

def get_battery_health_alert(batteryHealth):
    if batteryHealth < 30:
        return "Critical"
    elif batteryHealth < 70:
        return "Warning"
    else:
        return "Normal"

def listener(sample):
    try:
        payload = json.loads(sample.payload.to_string())
        print("Received from Zenoh:", payload)

        response = put_feature_value(THING_ID, "VehicleSpeed", payload["vehicleSpeed"])
        print("VehicleSpeed:", response.status_code)

        response = put_feature_value(THING_ID, "EngineSpeed", payload["engineSpeed"])
        print("EngineSpeed:", response.status_code)

        response = put_feature_value(THING_ID, "ThrottlePosition", payload["throttlePosition"])
        print("ThrottlePosition:", response.status_code)

        response = put_feature_value(THING_ID, "CoolantTemperature", payload["coolantTemperature"])
        print("CoolantTemperature:", response.status_code)

        response = put_feature_value(THING_ID, "BatteryHealth", payload["batteryHealth"])
        print("BatteryHealth:", response.status_code)

        overheatStatus = get_overheat_status(payload["coolantTemperature"])
        response = put_feature_value(THING_ID, "OverheatStatus", overheatStatus)
        print("OverheatStatus:", response.status_code)

        aggressiveDrivingScore = get_aggressive_driving_score(
            payload["vehicleSpeed"],
            payload["engineSpeed"],
            payload["throttlePosition"]
        )
        response = put_feature_value(THING_ID, "AggressiveDrivingScore", aggressiveDrivingScore)
        print("AggressiveDrivingScore:", response.status_code)

        batteryHealthAlert = get_battery_health_alert(payload["batteryHealth"])
        response = put_feature_value(THING_ID, "BatteryHealthAlert", batteryHealthAlert)
        print("BatteryHealthAlert:", response.status_code)

        print("-----------------------------")

    except Exception as e:
        print("Error handling sample:", e)

with zenoh.open(zenoh.Config()) as session:
    sub = session.declare_subscriber(ZENOH_KEY, listener)
    print(f"Subscribed to {ZENOH_KEY}")
    input("Press Enter to quit...\n")