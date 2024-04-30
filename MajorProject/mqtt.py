


import paho.mqtt.publish as publish



MQTT_SERVER = "172.28.202.183"  # MQTT broker address
MQTT_PATH = "file_transfer"  # Topic name

# Read the file content

with open("Data/sheets/data.xlsx","rb") as file:
    file_content = file.read()

# Publish the file content to the MQTT topic
publish.single(MQTT_PATH, payload=file_content, hostname=MQTT_SERVER)
