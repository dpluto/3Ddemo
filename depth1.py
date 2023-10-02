import numpy as np
import cv2
import os
import datetime
from openni import openni2

def mousecallback(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDBLCLK:
        print(y, x, dpt[y, x])

if __name__ == "__main__":
    save_path = "D:\\pluto\\Desktop\\depthimage"
    openni2.initialize()
    dev = openni2.Device.open_any()
    print(dev.get_device_info())
    depth_stream = dev.create_depth_stream()
    dev.set_image_registration_mode(True)
    depth_stream.start()
    cap = cv2.VideoCapture(1)
    cv2.namedWindow('depth')
    cv2.setMouseCallback('depth', mousecallback)
    while True:
        frame = depth_stream.read_frame()
        dframe_data = np.array(frame.get_buffer_as_triplet()).reshape([480, 640, 2])
        dpt1 = np.asarray(dframe_data[:, :, 0], dtype='float32')
        dpt2 = np.asarray(dframe_data[:, :, 1], dtype='float32')
        dpt2 *= 255
        dpt = dpt1 + dpt2

        dim_gray = cv2.convertScaleAbs(dpt, alpha=0.1275)
        depth_colormap = cv2.applyColorMap(dim_gray, 1)

        # Flip the depth colormap horizontally
        flipped_depth_colormap = cv2.flip(depth_colormap, 1)

        # Use timestamp to name and save the flipped depth image
        timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S%f')
        img_filename = os.path.join(save_path, f"flipped_depth_{timestamp}.png")
        cv2.imwrite(img_filename, flipped_depth_colormap)

        # Show the flipped depth image
        cv2.imshow('depth', flipped_depth_colormap)
        ret, frame = cap.read()

        key = cv2.waitKey(100)
        if int(key) == ord('q'):
            break

    depth_stream.stop()
    dev.close()