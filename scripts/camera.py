"""
Capture frames from a camera using jetcam and publish on an MQTT topic.
"""
import time
import os

from mqtt import get_mqtt_client
from helpers import get_now_string, get_config

from jetcam.csi_camera import CSICamera
from jetcam.utils import bgr8_to_jpeg

CONFIG_FILE_PATH = os.getenv("MQTT_CAMERA_CONFIG", "./config/config.yml")
CONFIG = get_config(CONFIG_FILE_PATH)

MQTT_BROKER = CONFIG["mqtt"]["broker"]
MQTT_PORT = CONFIG["mqtt"]["port"]
MQTT_QOS = CONFIG["mqtt"]["QOS"]

MQTT_TOPIC_CAMERA = CONFIG["camera"]["mqtt_topic"]
VIDEO_SOURCE = CONFIG["camera"]["vide_source"]
FPS = CONFIG["camera"]["fps"]


def main():
    client = get_mqtt_client()
    client.connect(MQTT_BROKER, port=MQTT_PORT)
    time.sleep(4)  # Wait for connection setup to complete
    client.loop_start()

    # Open camera
    camera = CSICamera(width=224, height=224, capture_width=3280, capture_height=2464, capture_fps=1)
    time.sleep(2)  # Webcam light should come on if using one

    while True:
        frame = camera.read()
        np_array_RGB = bgr8_to_jpeg(frame)

        client.publish(MQTT_TOPIC_CAMERA, np_array_RGB, qos=MQTT_QOS)
        now = get_now_string()
        print(f"published frame on topic: {MQTT_TOPIC_CAMERA} at {now}")
        time.sleep(1 / FPS)


if __name__ == "__main__":
    main()
