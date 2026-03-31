## 1. Project Overview and System Architecture

This project implements a simplified **Software-Defined Vehicle (SDV) telemetry pipeline** that demonstrates how vehicle data flows through multiple software components from the vehicle environment to a backend digital twin. A vehicle simulator generates telemetry signals such as vehicle speed, engine speed, throttle position, coolant temperature, and battery health.

The telemetry data is first processed by **Eclipse Kuksa**, which acts as the vehicle data abstraction layer and maintains the vehicle signal model. The data is then transported through **Eclipse Zenoh**, which serves as the communication middleware responsible for routing and transmitting telemetry between system components. Finally, the data is received by **Eclipse Ditto**, which maintains a digital twin representing the current state of the vehicle and updates it as new telemetry signals arrive.

This architecture demonstrates a complete SDV pipeline where vehicle data is generated, processed, transmitted, and stored across multiple system layers.

## 2. Required Software and Dependencies

To run this project, the following software and tools must be installed:

### Software
- Python 3.x
- Docker
- Eclipse Kuksa Databroker
- Eclipse Zenoh
- Eclipse Ditto

### Python Dependencies

All required Python libraries are listed in the `requirements.txt` file.  
They can be installed using:

pip install -r requirements.txt

## 3. Installation Instructions (Linux)

Follow these steps to install the required components on a Linux system.

### 1. Install Python and pip

sudo apt update
sudo apt install python3 python3-pip -y


### 2. Install Docker

Link: https://docs.docker.com/engine/install/

### 3. Install Zenoh

`curl -L https://github.com/eclipse-zenoh/zenoh/releases/latest/download/zenohd-linux-amd64 -o zenohd`

`chmod +x zenohd`

`sudo mv zenohd /usr/local/bin/`

### 4. Install Python Dependencies

`cd kuksa-databroker/kuksa-ditto`

`python -m venv env`

`source env/bin/activate`

`pip install -r requirements.txt`

### 5. Install Eclipse Ditto

`cd ditto/deployment/docker`

`docker compose up`

## Running the System

### Start up Kuksa with docker

`cd kuksa-databroker`

`docker run --rm -it -p 55556:55555 -v "$(pwd)/OBD.json:/OBD.json:ro" ghcr.io/eclipse-kuksa/kuksa-databroker:main --insecure --vss /OBD.json;2D`

### Start up Zenoh

`zenohd`

### Start up ditto (Only have to do this once, if already done during installation step then skip)

`cd ditto/deployment/docker`

`docker compose up`

### Run OBD Data to Kuksa Script

`cd kuksa-databroker/kuksa-ditto`

`source env/bin/activate`

`python send_obd_data_to_kuksa.py`

### Run Kuksa data to Zenoh Script

`cd kuksa-databroker/kuksa-ditto`

`source env/bin/activate`

`python kuksa_to_zenoh.py`

### Run Zenoh data to Ditto Script

`cd kuksa-databroker/kuksa-ditto`

`source env/bin/activate`

`python zenoh_to_ditto.py`
