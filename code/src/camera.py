from typing import TypedDict
from picamera2 import Picamera2
from picamer2.array import PiRGBArray
import numpy as np
from src.led import LED



class Config(TypedDict):
    # show_preview=True only works when having a graphical connection to the pi
    show_preview: bool


class Camera:
    cam: Picamera2
    image_array: np.ndarray

    def __init__(self, config: Config):
        self.green_led = LED(20)
        self.image_array = np.ndarray(0)

        try:
            self.cam = Picamera2()
            self.cam.start(show_preview=config['show_preview'])
        except:
            self.cam = None

    def capture(self):
        if self.cam != None:
            self.image_array = self.cam.capture_array()

    def read_qr_code(self):
        if self.cam is not None:
            # Capture image
            rawCapture = PiRBGArray(self.cam)
            self.cam.capture(rawCapture, format="bgr")
            image = rawCapture.array
            
            decoded_objects = pyzbar.decode(image)
            # Whenever QR code is found, turn Green LED on
            if decoded_objects:
                self.green_led.on()
                return decoded_objects
        return None
