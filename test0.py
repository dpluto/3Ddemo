from openni import openni2
import numpy as np
import cv2

if __name__ == "__main__":
    openni2.initialize()
    dev = openni2.Device.open_any()
    print(dev.get_device_info())