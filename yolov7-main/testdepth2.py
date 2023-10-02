import cv2
import numpy as np
from openni import openni2, nite2

def visualize_depth(depth_image):
    """归一化并应用伪彩色到深度图像"""
    depth_min = np.min(depth_image)
    depth_max = np.max(depth_image)
    normalized_depth = ((depth_image - depth_min) / (depth_max - depth_min) * 255).astype(np.uint8)
    colored_depth = cv2.applyColorMap(normalized_depth, cv2.COLORMAP_JET)
    return colored_depth

def initialize_openni():
    """初始化OpenNI并打开Orbbec Astra设备，返回设备和深度流"""
    openni2.initialize()
    dev = openni2.Device.open_any()
    depth_stream = dev.create_depth_stream()
    depth_stream.start()
    return dev, depth_stream

def process_depth_stream(depth_stream):
    """读取和处理深度流"""
    try:
        while True:
            frame = depth_stream.read_frame()
            frame_data = frame.get_buffer_as_uint16()
            depth_image = np.frombuffer(frame_data, dtype=np.uint16).reshape(frame.height, frame.width)
            colored_depth = visualize_depth(depth_image)
            filtered_depth = cv2.medianBlur(colored_depth, 5)
            cv2.imshow('Colored Depth Image', filtered_depth)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    finally:
        cv2.destroyAllWindows()

def main():
    dev, depth_stream = initialize_openni()
    try:
        process_depth_stream(depth_stream)
    finally:
        depth_stream.stop()
        dev.close()
        openni2.unload()

if __name__ == "__main__":
    main()